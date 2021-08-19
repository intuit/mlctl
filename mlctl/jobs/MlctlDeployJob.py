from random_words import RandomWords
import json

from mlctl.jobs.common.helper import parse_infrastructure, parse_resources

class MlctlDeployJob():

    def __init__(self, job_type, project, name=None):

        if name:
            # use the provided name
            self.name = name
        else:
            # else make a new name randomly
            word = RandomWords().random_word('d')
            self.name = f'mlctl-deploy-{word}'

        self.job_type = job_type
        self.project = project
        self.add_env_vars({'sriracha_run_name': self.name})
        
    
    def add_infra_provider(self, params):

        # take only the deploy values from the infrastructure
        self.infrastructure = parse_infrastructure(params)
        
        self.add_env_vars({
            'sriracha_provider': self.infrastructure['deploy']['name']
        })

    def add_models(self, params):
        # check if we already have models to add
        try:
            self.models
        except AttributeError:
            self.models = []

        # if there is a singular object, convert it to an array
        if 'artifact' in params:
            params = [params]
            
        for param in params:
            model = {
                'artifact': param['artifact']
            }

            try:
                model['name'] =  param['name']
            except KeyError:
                model['name'] = self.name

            # Add model traffic version
            try:
                model['traffic'] = param['traffic']
            except KeyError:
                model['traffic'] = 100

            # Add model version
            try:
                model['version'] = param['version']
            except KeyError:
                model['version'] = 1

            # add the model to models
            self.models.append(model)

        # verify models sum to 100
        traffic = 0
        for model in self.models:
            traffic += model['traffic']

        if traffic != 100:
            raise Exception('Traffic of models does not sum to 100.')

    def add_env_vars(self, params):
        try:
            self.env_vars
        except AttributeError:
            self.env_vars = {}

        env_vars = {}
        for key in params:
            # create all env vars with sriracha_ as prefix
            env_vars['sriracha_' + key] = params[key]

        self.env_vars.update(env_vars)
        
    def add_resources(self, params):

        # adding resource is designed to overwrite existing
        # As a ML engineer, I can override the provider specific YAML job
        if 'deploy' in params:
            self.infrastructure['deploy']['resources'] = parse_resources(params['deploy'])

        # if deploy add in autoscaling params
        if ('resources' in self.infrastructure['deploy'] and
        'instance_type' in self.infrastructure['deploy']['resources'] and 
        'instance_count_max' not in self.infrastructure['deploy']['resources']):
            self.infrastructure['deploy']['resources']['instance_count_max'] = 1

    def serialize(self):
        '''
        This function is used to return a serialized form of the deploy job created. 
        The intended use case is for plugins to parse the serialization
        and launch the upstream provider options
        '''
        return self.__dict__
    