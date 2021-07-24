import yaml
from pathlib import Path

from mlctl.interfaces.Training import Training
from mlctl.plugins.utils import parse_config
import subprocess

class AzureMlTraining(Training):
    # https://docs.microsoft.com/en-us/cli/azure/ml/job?view=azure-cli-latest#code-try-9
    def __init__(self, profile=None):
        self.provider = 'azureml'

    def start_training(self, job):
        
        job_definition = job.serialize()
        workspace_name = job_definition['infrastructure']['workspace_name']
        sriracha_provider = job_definition['env_vars']['sriracha_provider']

        input = {}
        for channel in ['training', 'validation', 'testing']:
            if channel in job_definition['data_channels']['input']:
                input[channel] = {
                    'data': {'path': job_definition['data_channels']['input'][channel]},
                    'mode': 'mount'
                }
        # build yaml
        azure_yaml = {
            '$schema': 'https://azuremlschemas.azureedge.net/latest/commandJob.schema.json',
            'command': f'python /opt/main.py --set sriracha_provider={sriracha_provider}',
            'environment': {
                'name': job_definition['name'],
                'docker': {
                    # hardcoding image until we have a mlctl state system for tracking tags
                    'image': job_definition['infrastructure']['container_repo'] + ':train-image',
                }
            },
            'inputs': input,
            'environment_variables': job_definition['env_vars'],
            'compute': {
                'target': f'azureml:{workspace_name}'
            }
        }


        # save yaml in cache
        Path("./.mlctl/azureml").mkdir(parents=True, exist_ok=True)
        with open('./.mlctl/azureml/train.yaml', 'w') as outfile:
            yaml.dump(azure_yaml, outfile, default_flow_style=False)

        resource_group = job_definition['infrastructure']['resource_group']
        process = subprocess.Popen(['az', 'ml', 'job', 'create', '-f', './.mlctl/azureml/train.yaml', '--web',
        '--resource-group', resource_group, '--workspace-name', workspace_name],
        stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if process.poll() is not None:
                break
            if output:
                print (output.strip())
        retval = process.poll()

    def get_training_info(self, training_job_name, hyperparameter_tuning=False):
        try:
            # 
            process = subprocess.Popen(['az', 'ml', 'job', 'show', '--name', training_job_name, '--query' 
            '{Name:name,Jobstatus:status}', '--output', 'table', '--resource-group', resource_group,
            '--workspace-name', workspace_name], stdout=subprocess.PIPE)
            while True:
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                if output:
                    print (output.strip().encode("utf-8"))
            retval = process.poll()
        except Exception as e:
            return str(e)

    def stop_training(self, training_job_name, hyperparameter_tuning=False):
        try:
            # az ml job cancel --name --resource-group --workspace-name
            # 
            process = subprocess.Popen(['az', 'ml', 'job', 'cancel', '--name', training_job_name,
            '--resource-group', resource_group, '--workspace-name', workspace_name],
            stdout=subprocess.PIPE)
            while True:
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                if output:
                    print (output.strip())
            retval = process.poll()
        except Exception as e:
            return str(e)
