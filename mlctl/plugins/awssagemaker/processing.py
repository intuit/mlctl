from mlctl.interfaces.Processing import Processing
from mlctl.plugins.utils import parse_config
import boto3


class AwsSagemakerProcessing(Processing):

    def __init__(self, profile=None):
        if profile:
            boto3.setup_default_session(profile_name=profile)
        self._client = boto3.client("sagemaker")

    def start_processing(self, job):
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

            # https://docs.aws.amazon.com/sagemaker/latest/dg/build-your-own-processing-container.html
            kwargs = {
                'ProcessingJobName': job_definition['name'],
                
                'AppSpecification': {
                    # hardcoding image until we have a mlctl state system for tracking tags
                    'ImageUri': job_definition['infrastructure']['processing']['container_repo'] + ':processing-image'
                }, 
                'Environment': job_definition['env_vars'],
                'ProcessingInputs': [{
                    # TODO: support for multiple input channels
                    'InputName': 'input-1',
                    'S3Input': {
                        'LocalPath': "/opt/ml/processing/inputs/",
                        'S3DataType': 'S3Prefix',
                        'S3Uri': job_definition['data_channels']['input']['processing'],
                        'S3DataDistributionType': 'FullyReplicated',
                        # 'ContentType': 'text/csv',
                        'S3InputMode': 'File',
                    },
                }], 'ProcessingOutputConfig': {
                    'Outputs': [{
                        'OutputName': 'output-1',
                        'S3Output': {
                            'LocalPath': '/opt/ml/processing/outputs/',
                            "S3Uri": job_definition['data_channels']['output'],
                            "S3UploadMode": "EndOfJob"
                        }
                    }]
                }, 'ProcessingResources': {
                    'ClusterConfig': {
                        'InstanceType': job_definition['infrastructure']['processing']['resources']['instance_type'],
                        'InstanceCount': job_definition['infrastructure']['processing']['resources']['instance_count'],
                        'VolumeSizeInGB': 30
                    }
                },'Tags': [{
                    'Key': 'mlctl',
                    # to update
                    'Value': '0.0.1'
                }], 
                'RoleArn': job_definition['infrastructure']['processing']['arn'],
                'StoppingCondition': {
                    'MaxRuntimeInSeconds': 10800
                }
            }

            response = self._client.create_processing_job(
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

    def get_processing_info(self, training_job_name, hyperparameter_tuning=False):
        pass

    def stop_processing(self, training_job_name, hyperparameter_tuning=False):
        pass