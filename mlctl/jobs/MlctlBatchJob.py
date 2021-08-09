from random_word import RandomWords
import json

from mlctl.jobs.common.helper import parse_infrastructure, parse_resources

class MlctlTrainingJob():

    def __init__(self, job_type, project, name=None):

        if name:
            # use the provided name
            self.name = name
        else:
            # else make a new name randomly
            words = RandomWords().get_random_words()
            self.name = f'mlctl-{words[0]}-{words[1]}'

        self.job_type = job_type
        self.project = project
        self.add_env_vars({'sriracha_run_name': self.name, 'sriracha_experiment_name': project})
    
    def add_infra_provider(self, params):
        
        # TODO: convert to diction with default and then training/hosting/specific

        # TODO: add validation on allowed infrastructure
        self.infrastructure = {'name': params['name']}
        self.infrastructure['container_repo'] = params['container_repo']

        # currently used for AWS
        if 'arn' in params:
            self.infrastructure['arn'] = params['arn']

        # currently used for Azure
        if 'resource_group' in params:
            self.infrastructure['resource_group'] = params['resource_group']
        
        if 'workspace_name' in params:
            self.infrastructure['workspace_name'] = params['workspace_name']
        
        if type(params) == str:
            self.infrastructure['instance_type'] = params
            self.infrastructure['instance_count'] = 1
        elif 'instance' in params:
            self.infrastructure['instance_type'] = params.instance 
            self.infrastructure['instance_count'] = params.count
        elif 'cpu' in params:
            self.infrastructure['cpu'] = params.cpu
            self.infrastructure['memory'] = params.memory

        self.add_env_vars({
            'sriracha_provider': params['name']
        })

    def add_metadata_provider(self, params):

        try:
            self.metadata
        except AttributeError:
            self.metadata = []

        self.metadata.append({
            'name': params['name'],
            'tracking_uri': params['tracking_uri']
        })

    def add_monitor_providers():
        pass

    def add_data_channels(self, params):

        # define the placeholder
        try:
            self.data_channels
        except AttributeError:
            self.data_channels = {
                'input': {},
            }

        # if the user only puts a string, default to training
        if type(params['input']) == str: 
            self.data_channels['input'].update({
                'training': params['input']
            })
        else:
            self.data_channels['input'].update(params['input'])

        # if there is a desired storage output
        if params['output']:
            self.data_channels['output'] = params['output']
            

    def add_env_vars(self, params):
        try:
            self.env_vars
        except AttributeError:
            self.env_vars = {}
        
        try:
            self.hyperparameters
        except AttributeError:
            self.hyperparameters = {}

        env_vars = {}
        hyperparameters = {}

        # hyperparameter values are denoted as 'hp_'
        # store without 'hp_
        for key in params:
            if key.startswith('hp_'):
                hyperparameters[key[3:]] = params[key]
            else:
                env_vars[key] = params[key]

        self.env_vars.update(env_vars)
        self.hyperparameters.update(hyperparameters)
        

    def add_resources(self, params):

        # adding resource is designed to overwrite existing
        # As a ML engineer, I can override the provider specific YAML job
            if 'batch' in params:
                self.infrastructure['batch']['resources'] = parse_resources(params['batch'])

    def serialize(self):
        return self.__dict__
    