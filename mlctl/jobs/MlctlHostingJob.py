from random_word import RandomWords
import json

from mlctl.jobs.common.helper import parse_infrastructure

class MlctlHostingJob():

    def __init__(self, job_type, project, name=None):

        if name:
            # use the provided name
            self.name = name
        else:
            # else make a new name randomly
            words = RandomWords().get_random_words()
            self.name = f'mlctl-hosting-{words[0]}'

        self.job_type = job_type
        self.project = project
        self.add_env_vars({'sriracha_run_name': self.name})
        
    
    def add_infra_provider(self, params):

        # take only the hosting values from the infrastructure
        self.infrastructure = parse_infrastructure(params)
        
        self.add_env_vars({
            'sriracha_provider': self.infrastructure['hosting']['name']
        })

    def add_models(self, params):

        try:
            self.models
        except AttributeError:
            self.models = []

        for param in params:
            model = {
                'name': param['name'],
                'artifact': param['artifact']
            }

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
            env_vars[key] = params[key]

        self.env_vars.update(env_vars)
        
    def add_resources(self, params):

        # adding resource is designed to overwrite existing
        self.infrastructure['hosting']['resources'] = {}

        if type(params) == str:
            self.infrastructure['hosting']['resources']['instance_type'] = params
            self.infrastructure['hosting']['resources']['instance_count'] = 1
        elif 'instance' in params:
            self.infrastructure['hosting']['resources']['instance_type'] = params.instance 
            self.infrastructure['hosting']['resources']['instance_count'] = params.count
        elif 'cpu' in params:
            self.infrastructure['hosting']['resources']['cpu'] = params.cpu
            self.infrastructure['hosting']['resources']['memory'] = params.memory

        # if hosting add in autoscaling params
        if ('resources' in self.infrastructure['hosting'] and
        'instance_type' in self.infrastructure['hosting']['resources'] and 
        'instance_count_max' not in self.infrastructure['hosting']['resources']):
            self.infrastructure['hosting']['resources']['instance_count_max'] = 1

    def serialize(self):
        '''
        This function is used to return a serialized form of the Hosting job created. 
        The intended use case is for plugins to parse the serialization
        and launch the upstream provider options
        '''
        return self.__dict__
    