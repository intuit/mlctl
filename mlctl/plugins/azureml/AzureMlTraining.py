from mlctl.interfaces.Training import Training
from mlctl.plugins.utils import parse_config
import subprocess

class AzureMlTraining(Training):
    # https://docs.microsoft.com/en-us/cli/azure/ml/job?view=azure-cli-latest#code-try-9
    def __init__(self, profile=None):
        self.provider = 'azureml'

    def start_training(self, config):
        # TODO build train.yaml
        resource_group = 'mlctl'
        workspace_name = 'mlctl-test'
        process = subprocess.Popen(f'az ml job create -f ./dist/azureml/train.yaml --web \
        --resource-group {resource_group} --workspace-name {workspace_name}',
        stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if process.poll() is not None and output == '':
                break
            if output:
                print (output.strip())
        retval = process.poll()

    def get_training_info(self, training_job_name):
        try:
            # 
            process = subprocess.Popen(f'az ml job show --name {training_job_name} --query \
            "{{Name:name,Jobstatus:status}}"  --output table \
            --resource-group {resource_group} --workspace-name {workspace_name}',
            stdout=subprocess.PIPE)
            while True:
                output = process.stdout.readline()
                if process.poll() is not None and output == '':
                    break
                if output:
                    print (output.strip())
            retval = process.poll()
        except Exception as e:
            return str(e)

    def stop_training(self, training_job_name):
        try:
            # az ml job cancel --name --resource-group --workspace-name
            # 
            process = subprocess.Popen(f'az ml job cancel --name {training_job_name} \
            --resource-group {resource_group} --workspace-name {workspace_name}',
            stdout=subprocess.PIPE)
            while True:
                output = process.stdout.readline()
                if process.poll() is not None and output == '':
                    break
                if output:
                    print (output.strip())
            retval = process.poll()
        except Exception as e:
            return str(e)
