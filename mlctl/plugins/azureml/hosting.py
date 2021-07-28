import yaml
from pathlib import Path
from distutils.core import run_setup

from mlctl.interfaces.Hosting import Hosting
from mlctl.plugins.utils import parse_config, run_subprocess


class AzureMlHosting(Hosting):
    # https://docs.microsoft.com/en-us/cli/azure/ml/job?view=azure-cli-latest#code-try-9
    def __init__(self, profile=None):
        self.provider = 'azureml'

    def create(self, job):
        pass

    def start_hosting(self, job):
        
        job_definition = job.serialize()
            
        hosting_job_name = job_definition['name']
        resource_group = job_definition['infrastructure']['hosting']['resource_group']
        workspace_name = job_definition['infrastructure']['hosting']['workspace_name']

        sriracha_provider = job_definition['env_vars']['sriracha_provider']

        ###########
        # parse setup.py to get the entrypoint data

        result = run_setup("./setup.py", stop_after="init")
        prediction_entrypoint = result.entry_points['baklava.predict'][0]
        # input: {'baklava.predict': ['my_prediction_entrypoint = sklearn_tree.predict:main']}
        # output: sklearn_tree

        # find =
        equal_sign = prediction_entrypoint.find('=') + 1
        # find .
        dot_sign = prediction_entrypoint.find('.', equal_sign)
        # find :
        colon_sign = prediction_entrypoint.find(':', equal_sign)

        # find the folder name
        folder_name = prediction_entrypoint[equal_sign: dot_sign].strip()
        # find the file name 
        file_name = prediction_entrypoint[dot_sign + 1: colon_sign].strip()

        ###########
        
        
        # build the traffic and deployment objects using this loop
        traffic = {}
        deployments = []

        for model in job_definition['models']:
            traffic.update({
                model['name']: model['traffic']
            })

            ###########
            # Download the artifact for submission to the Az ML cluster
            
            # The URI to storage account, storage container, and file name
            # input: https://mlctldata.blob.core.windows.net/modelartifact/model.pkl
            # output: storage_account, container_account, file_name

            model_uri = model['artifact'].replace('https://', '')

            storage_account = model_uri[0: model_uri.find('.')]
            container_account = model_uri[model_uri.find('/') + 1: model_uri.rfind('/')]
            model_file_name = model_uri[model_uri.rfind('/') + 1: len(model_uri)]
            print(f'Retrieving artifact for submission to Azure ML cluster: {storage_account} {container_account} {model_file_name}')

            # download the file from Azure blob
            Path("./.mlctl/azureml").mkdir(parents=True, exist_ok=True)
            Path("./.mlctl/azureml/data").mkdir(parents=True, exist_ok=True)
            run_subprocess(['az', 'storage', 'blob', 'download', '--account-name', storage_account ,'-c', container_account, '-f', f'.mlctl/azureml/data/{model_file_name}', '-n', model_file_name])

            ###########

            deployments.append({
                'name': model['name'],
                'model': {
                    'name': model['name'],
                    'version': 1,
                    'local_path': f'./data/{model_file_name}'
                }, 'code_configuration': {
                    'code': {
                        # azure SDK assumes the YAML location, so move up 2 directories to back to main
                        'local_path': f'../../{folder_name}/'
                    }, 
                    'scoring_script': f'{file_name}.py'
                }, 'environment': {
                    'name': model['name'],
                    'version': 1,
                    'docker':{
                        # TODO: make this image repo/tag dynamic
                        'image': job_definition['infrastructure']['hosting']['container_repo'] + ':predict-image'
                    }, 'inference_config': {
                        'liveness_route': {
                            'port': 8080,
                            'path': '/ping'
                        }, 'readiness_route': {
                            'port': 8080,
                            'path': '/ping'
                        }, 'scoring_route': {
                            'port': 8080,
                            'path': '/invocations'
                        }
                            
                    }
                },
                'instance_type': job_definition['infrastructure']['hosting']['resources']['instance_type'],
                'scale_settings': {
                    'scale_type': 'manual',
                    'instance_count': 1,
                    'min_instances': 1,
                    'max_instances': job_definition['infrastructure']['hosting']['resources']['instance_count_max']
                }
            })

        # build yaml
        azure_yaml = {
            '$schema': 'https://azuremlsdk2.blob.core.windows.net/latest/managedOnlineEndpoint.schema.json',
            'name': job_definition['name'],
            'type': 'online',
            'auth_mode': 'key',
            'traffic': traffic,
            'deployments': deployments
        }


        # save yaml in cache
        with open('./.mlctl/azureml/hosting.yaml', 'w') as outfile:
            yaml.dump(azure_yaml, outfile, default_flow_style=False)

        # az ml endpoint create --name sklearnendpoint -f endpoint.yaml  --resource-group mlctl --workspace-name mlctl-test
        run_subprocess(['az', 'ml', 'endpoint', 'create', '--name', hosting_job_name, '-f', './.mlctl/azureml/hosting.yaml',
        '--resource-group', resource_group, '--workspace-name', workspace_name])

    def get_hosting_info(self, job):
        try:
            # 
            job_definition = job.serialize()
            
            hosting_job_name = job_definition['name']
            resource_group = job_definition['infrastructure']['hosting']['resource_group']
            workspace_name = job_definition['infrastructure']['hosting']['workspace_name']

            run_subprocess(['az', 'ml', 'job', 'show', '--name', training_job_name, '--query' 
            '{Name:name,Jobstatus:status}', '--output', 'table', '--resource-group', resource_group,
            '--workspace-name', workspace_name])
        except Exception as e:
            return str(e)

    def stop_hosting(self, job):
        try:
            # az ml job cancel --name --resource-group --workspace-name
            # 
            job_definition = job.serialize()
            
            hosting_job_name = job_definition['name']
            resource_group = job_definition['infrastructure']['hosting']['resource_group']
            workspace_name = job_definition['infrastructure']['hosting']['workspace_name']

            run_subprocess(['az', 'ml', 'job', 'cancel', '--name', hosting_job_name,
            '--resource-group', resource_group, '--workspace-name', workspace_name])
        except Exception as e:
            return str(e)
