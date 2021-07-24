import yaml

from mlctl.plugins.sagemaker.SagemakerBatch import SagemakerBatch
from mlctl.plugins.sagemaker.SagemakerHosting import SagemakerHosting
from mlctl.plugins.awssagemaker.training import AwsSagemakerTraining
import mlctl.plugins.mlflow.metadata as MlflowPlugin
from mlctl.plugins.azureml.training import AzureMlTraining
from mlctl.interfaces.MlctlTrainingJob import MlctlTrainingJob

def parse_yamls(job_config, provider_config=None):

    
    if provider_config:
        # if the user provides a specific config file
        provider_file = provider_config
    else: 
        # else load from the local directory provider.yaml spot
        provider_file = './provider.yaml'

    # load all yamls
    with open(provider_file) as f:
        provider_spec = yaml.safe_load(f)
    
    with open(job_config) as f:
        job_spec = yaml.safe_load(f)

    # print(provider_spec)
    # print(job_spec)

    try:
        # job name is optional 
        # TODO: clean this function to parse for job_name requirement
        job = MlctlTrainingJob(job_spec['metadata']['job_type'], job_spec['metadata']['project'], job_spec['metadata']['job_name'])
    except KeyError:
        job = MlctlTrainingJob(job_spec['metadata']['job_type'], job_spec['metadata']['project'])
    job.add_data_channels(job_spec['data'])

    if 'resources' in provider_spec:
        job.add_resources(provider_spec['resources'])
    if 'resources' in job_spec:
        job.add_resources(job_spec['resources'])

    if 'env_vars' in job_spec: 
        job.add_env_vars(job_spec['env_vars'])
    
    if 'env_vars' in provider_spec:
        job.add_env_vars(provider_spec['env_vars'])

    job.add_infra_provider(provider_spec['infrastructure'])

    print(job.serialize())

    # add metadata loggers
    if 'metadata' in provider_spec:
        for metadata in provider_spec['metadata']:
            job.add_metadata_provider(metadata)
    
            # TODO: make this generalized instead of hardcoding
            if(metadata['name'] == 'mlflow'):
                job = MlflowPlugin.sriracha_bootstrapping(metadata, job)
 
    


    return job

def determine_infra_plugin_from_job(job, profile=None):
    job_definition = job.serialize()

    if job_definition['infrastructure']['name'] == 'awssagemaker':
        job_type = job_definition['job_type']
        if job_definition['job_type'] == 'batch':
            return SagemakerBatch(profile)
        elif job_definition['job_type'] == 'hosting':
            return SagemakerHosting(profile)
        elif job_definition['job_type'] == 'training':
            return AwsSagemakerTraining(profile)
        else:
            print(f'{job_type} is not a valid job')
    elif job_definition['infrastructure']['name'] == 'azureml':
        if job_definition['job_type'] == 'training':
            return AzureMlTraining(profile)

# Used for old versions of CLI
def determine_plugin(plugin, profile, capability):
    if plugin == 'sagemaker':
        if capability == 'batch':
            return SagemakerBatch(profile)
        elif capability == 'hosting':
            return SagemakerHosting(profile)
        elif capability == 'training':
            return SagemakerTraining(profile)
        else:
            print(f'{capability} is not a valid job')
    elif plugin == 'azureml':
        if capability == 'training':
            return AzureMlTraining(profile)