from mlctl.interfaces.train import Train
from mlctl.plugins.utils import parse_config
import boto3

class AwsSagemakerTrain(Train):

    def __init__(self, profile=None):
        if profile:
            boto3.setup_default_session(profile_name=profile)
        self._client = boto3.client("sagemaker")

    def start_train(self, job):
        try:
            # if hyperparameter_tuning == True:
            #     parameters = ["HyperParameterTuningJobName",
            #                   "HyperParameterTuningJobConfig",
            #                   "TrainingJobDefinition",
            #                   "TrainingJobDefinitions",
            #                   "WarmStartConfig",
            #                   "Tags"]
            #     kwargs = parse_config(config, parameters)
            #     return self._client.create_hyper_parameter_tuning_job(
            #         **{k: v for k, v in kwargs.items() if v is not None})

            # else:
            job_definition = job.serialize()

            # converts everything to string for boto3 API
            hyperparameters = {}
            for key in job_definition['hyperparameters']:
                hyperparameters[key.replace('sriracha_hp_', '')] = str(job_definition['hyperparameters'][key])

            kwargs = {
                'TrainingJobName': job_definition['name'],
                'RoleArn': job_definition['infrastructure']['train']['arn'],
                'AlgorithmSpecification': {
                    # TODO: support various image tags
                    'TrainingImage': job_definition['infrastructure']['train']['container_repo'] + ':train-image',
                    'TrainingInputMode': 'File'
                }, 'InputDataConfig': [{
                    # TODO: support multiple channels
                    'ChannelName': 'training',
                    'DataSource': {
                        'S3DataSource': {
                            'S3DataType': 'S3Prefix',
                            'S3Uri': job_definition['data_channels']['input']['train'],
                            'S3DataDistributionType': 'FullyReplicated',
                        }
                    },
                    'ContentType': 'text/csv',
                    'InputMode': 'File',
                }], 'OutputDataConfig': {
                    'S3OutputPath': job_definition['data_channels']['output']
                }, 'ResourceConfig': {
                    'InstanceType': job_definition['infrastructure']['train']['resources']['instance_type'],
                    'InstanceCount': job_definition['infrastructure']['train']['resources']['instance_count'],
                    'VolumeSizeInGB': 30
                },'Tags': [{
                    'Key': 'mlctl',
                    # to update
                    'Value': '0.0.1'
                }], 'Environment': job_definition['env_vars'],
                'HyperParameters': hyperparameters,
                'StoppingCondition': {
                    'MaxRuntimeInSeconds': 10800
                }
            }

            response = self._client.create_training_job(
                **{k: v for k, v in kwargs.items() if v is not None}
            )
            # print()
            return response
            # return self._client.create_training_job(
            #     **{k: v for k, v in kwargs.items() if v is not None}
            # )
        except Exception as e:
            print('Error' + e)
            return str(e)

    def get_train_info(self, train_job_name):
        pass

    def stop_train(self, train_job_name):
        pass