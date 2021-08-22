import yaml

from mlctl.plugins.awssagemaker.deploy import AwsSagemakerDeploy
from mlctl.plugins.awssagemaker.train import AwsSagemakerTrain
from mlctl.plugins.awssagemaker.process import AwsSagemakerProcess
from mlctl.plugins.azureml.train import AzureMlTrain
from mlctl.plugins.azureml.deploy import AzureMlDeploy
from mlctl.plugins.kubernetes.train import KubernetesTrain
import mlctl.plugins.mlflow.metadata as MlflowPlugin

from mlctl.jobs.MlctlTrainJob import MlctlTrainJob
from mlctl.jobs.MlctlDeployJob import MlctlDeployJob
from mlctl.jobs.MlctlProcessJob import MlctlProcessJob

def docker_instructions(image_name):
    return f'\nThe container was built with tag {image_name}. \
To start the container on a service, tag your image to your remote repository \
and then push the container. \
The Docker commands should look like:\n\n\
docker tag {image_name} [remote_repository]\n\
docker push [remote_repository]'

def parse_process_yamls(job_config, provider_config=None):

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

    if job_spec['metadata']['job_type'] != 'process':
        job_type = job_spec['metadata']['job_type']
        raise Exception(f'You are attempting to start a process job with a {job_type} YAML')

    try:
        # job name is optional 
        # TODO: clean this function to parse for job_name requirement
        job = MlctlProcessJob(job_spec['metadata']['job_type'], job_spec['metadata']['project'], job_spec['metadata']['job_name'])
    except KeyError:
        job = MlctlProcessJob(job_spec['metadata']['job_type'], job_spec['metadata']['project'])
    job.add_data_channels(job_spec['data'])

    job.add_infra_provider(provider_spec['infrastructure'])

    if 'resources' in provider_spec:
        print(provider_spec['resources'])
        job.add_resources(provider_spec['resources'])

    if 'resources' in job_spec:
        job.add_resources(job_spec['resources'])

    if 'env_vars' in job_spec: 
        job.add_env_vars(job_spec['env_vars'])
    
    if 'env_vars' in provider_spec:
        job.add_env_vars(provider_spec['env_vars'])


    # add metadata loggers
    if 'metadata' in provider_spec:
        for metadata in provider_spec['metadata']:
            job.add_metadata_provider(metadata)
    
            # TODO: make this generalized instead of hardcoding
            if(metadata['name'] == 'mlflow'):
                job = MlflowPlugin.sriracha_bootstrapping(metadata, job)
 
    print(job.serialize())

    return job

def parse_train_yamls(job_config, provider_config=None):
    
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

    if job_spec['metadata']['job_type'] != 'train':
        job_type = job_spec['metadata']['job_type']
        raise Exception(f'You are attempting to start a train job with a {job_type} YAML')

    try:
        # job name is optional 
        # TODO: clean this function to parse for job_name requirement
        job = MlctlTrainJob(job_spec['metadata']['job_type'], job_spec['metadata']['project'], job_spec['metadata']['job_name'])
    except KeyError:
        job = MlctlTrainJob(job_spec['metadata']['job_type'], job_spec['metadata']['project'])
    job.add_data_channels(job_spec['data'])

    job.add_infra_provider(provider_spec['infrastructure'])

    if 'resources' in provider_spec:
        job.add_resources(provider_spec['resources'])

    if 'resources' in job_spec:
        job.add_resources(job_spec['resources'])

    if 'env_vars' in job_spec: 
        job.add_env_vars(job_spec['env_vars'])
    
    if 'env_vars' in provider_spec:
        job.add_env_vars(provider_spec['env_vars'])


    # add metadata loggers
    if 'metadata' in provider_spec:
        for metadata in provider_spec['metadata']:
            job.add_metadata_provider(metadata)
    
            # TODO: make this generalized instead of hardcoding
            if(metadata['name'] == 'mlflow'):
                job = MlflowPlugin.sriracha_bootstrapping(metadata, job)
 
    print(job.serialize())

    return job

def parse_deploy_yamls(job_config, provider_config=None):

    
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

    if job_spec['metadata']['job_type'] != 'deploy':
        job_type = job_spec['metadata']['job_type']
        raise Exception(f'You are attempting to start a deploy job with a {job_type} YAML')

    try:
        # job name is optional 
        # TODO: clean this function to parse for job_name requirement
        job = MlctlDeployJob(job_spec['metadata']['job_type'], job_spec['metadata']['project'], job_spec['metadata']['job_name'])
    except KeyError:
        job = MlctlDeployJob(job_spec['metadata']['job_type'], job_spec['metadata']['project'])

    # Add the infra details from the provider first
    job.add_infra_provider(provider_spec['infrastructure'])
    
    if 'resources' in provider_spec:
        job.add_resources(provider_spec['resources'])

    # Follow up second with the resources from the job YAML if the user wants to override
    if 'resources' in job_spec:
        job.add_resources(job_spec['resources'])

    if 'env_vars' in job_spec: 
        job.add_env_vars(job_spec['env_vars'])
    
    if 'env_vars' in provider_spec:
        job.add_env_vars(provider_spec['env_vars'])

    
    job.add_models(job_spec['models'])

    print(job.serialize())
 
    return job

def determine_infra_plugin_from_job(job, profile=None):
    job_definition = job.serialize()

    if job_definition['infrastructure'][job_definition['job_type']]['name'] == 'awssagemaker':
        job_type = job_definition['job_type']
        if job_definition['job_type'] == 'batch':
            # TODO: reimplement batch
            return
        elif job_definition['job_type'] == 'deploy':
            return AwsSagemakerDeploy(profile)
        elif job_definition['job_type'] == 'train':
            return AwsSagemakerTrain(profile)
        elif job_definition['job_type'] == 'process':
            return AwsSagemakerProcess(profile)
        else:
            print(f'{job_type} is not a valid job')
    elif job_definition['infrastructure'][job_definition['job_type']]['name'] == 'azureml':
        if job_definition['job_type'] == 'train':
            return AzureMlTrain(profile)
        elif job_definition['job_type'] == 'deploy':
            return AzureMlDeploy(profile)
    elif job_definition['infrastructure'][job_definition['job_type']]['name'] == 'kubernetes':
        if job_definition['job_type'] == 'train':
            return KubernetesTrain(profile)

    raise Error('No infrastructure plug in found') 