import yaml
from pathlib import Path

from mlctl.interfaces.train import Train
from mlctl.plugins.utils import parse_config, run_subprocess
import subprocess

class AzureMlTrain(Train):
    # https://docs.microsoft.com/en-us/cli/azure/ml/job?view=azure-cli-latest#code-try-9
    def __init__(self, profile=None):
        self.provider = 'azureml'

    def start_train(self, job):
        
        job_definition = job.serialize()
        workspace_name = job_definition['infrastructure']['train']['workspace_name']
        sriracha_provider = job_definition['env_vars']['sriracha_provider']

        # create the env variable payload
        env_vars = {}
        
        for k, v in job_definition['hyperparameters'].items():
            env_vars['sriracha_hp_' + k] = v

        env_vars.update(job_definition['env_vars'])

        # convert everything to string
        env_vars = {k: str(env_vars[k]) for k in env_vars}

        # create the data payload
        input = {}
        command_input = ''
        for channel in ['training', 'validation', 'testing']:
            if channel in job_definition['data_channels']['input']:
                input[channel] = {
                    'data': {'path': job_definition['data_channels']['input'][channel]},
                    'mode': 'mount'
                }
                command_input += f' {channel}-data={{inputs.{channel}}}'
        # build yaml
        azure_yaml = {
            '$schema': 'https://azuremlschemas.azureedge.net/latest/commandJob.schema.json',
            'command': f'python /opt/main.py --set sriracha_provider={sriracha_provider}{command_input}',
            'environment': {
                'name': job_definition['name'],
                'docker': {
                    # hardcoding image until we have a mlctl state system for tracking tags
                    'image': job_definition['infrastructure']['train']['container_repo'] + ':train-image',
                }
            },
            'inputs': input,
            'environment_variables': env_vars,
            'compute': {
                'target': f'azureml:{workspace_name}'
            }
        }


        # save yaml in cache
        Path("./.mlctl/azureml").mkdir(parents=True, exist_ok=True)
        with open('./.mlctl/azureml/train.yaml', 'w') as outfile:
            yaml.dump(azure_yaml, outfile, default_flow_style=False)

        resource_group = job_definition['infrastructure']['train']['resource_group']
        run_subprocess(['az', 'ml', 'job', 'create', '-f', './.mlctl/azureml/train.yaml', '--web',
        '--resource-group', resource_group, '--workspace-name', workspace_name])

    def get_train_info(self, train_job_name, hyperparameter_tuning=False):
        try:
            # 
            run_subprocess(['az', 'ml', 'job', 'show', '--name', train_job_name, '--query' 
            '{Name:name,Jobstatus:status}', '--output', 'table', '--resource-group', resource_group,
            '--workspace-name', workspace_name])
            while True:
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                if output:
                    print (output.strip().encode("utf-8"))
            retval = process.poll()
        except Exception as e:
            return str(e)

    def stop_train(self, train_job_name, hyperparameter_tuning=False):
        try:
            # az ml job cancel --name --resource-group --workspace-name
            # 
            run_subprocess(['az', 'ml', 'job', 'cancel', '--name', train_job_name,
            '--resource-group', resource_group, '--workspace-name', workspace_name])
            while True:
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                if output:
                    print (output.strip())
            retval = process.poll()
        except Exception as e:
            return str(e)
