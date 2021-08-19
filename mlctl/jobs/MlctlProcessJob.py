from random_words import RandomWords
import json

from mlctl.jobs.common.helper import parse_infrastructure, parse_resources

class MlctlProcessJob():

    def __init__(self, job_type, project, name=None):

        if name:
            # use the provided name
            self.name = name
        else:
            # else make a new name randomly
            word = RandomWords().random_word()
            self.name = f'mlctl-process-{word}'

        self.job_type = job_type
        self.project = project
        self.add_env_vars({'run_name': self.name, 'experiment_name': project})
    
    def add_infra_provider(self, params):
    
        self.infrastructure = parse_infrastructure(params) 
        
        self.add_env_vars({
            'provider': self.infrastructure['process']['name']
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

        # if the user only puts a string, default to process
        if type(params['input']) == str: 
            self.data_channels['input'].update({
                'process': params['input']
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
                # copy the values to hyperparameters without hp_
                hyperparameters[key[3:]] = params[key]
            else:
                # create all env vars with sriracha_ as prefix
                env_vars['sriracha_' + key] = params[key]

        self.env_vars.update(env_vars)
        self.hyperparameters.update(hyperparameters)
        

    def add_resources(self, params):

        # adding resource is designed to overwrite existing
        # As a ML engineer, I can override the provider specific YAML job
        if 'process' in params:
            # print(params)
            self.infrastructure['process']['resources'] = parse_resources(params['process'])

    def serialize(self):
        return self.__dict__
    