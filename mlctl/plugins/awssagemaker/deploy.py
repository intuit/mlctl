import yaml
from pathlib import Path
import boto3
from distutils.core import run_setup

from mlctl.interfaces.deploy import Deploy
from mlctl.plugins.utils import parse_config, run_subprocess


class AwsSagemakerDeploy(Deploy):
    def __init__(self, profile=None):
        self.provider = 'awssagemaker'

        self.client = boto3.Session().client('sagemaker')

    def create(self, job):
        job_definition = job.serialize()

        variants = []
        for model in job_definition['models']:

            response = self.client.create_model(
                ModelName=model['name']+ '-model',
                PrimaryContainer={
                    'Image': job_definition['infrastructure']['deploy']['container_repo'] + ':predict-image',
                    'ImageConfig': {
                        'RepositoryAccessMode': 'Platform',
                    },
                    'Mode': 'SingleModel',
                    'ModelDataUrl': model['artifact'],
                    'Environment': {
                        'sriracha_provider': 'awssagemaker'
                    },
                },
                ExecutionRoleArn= job_definition['infrastructure']['deploy']['arn'],
                Tags=[
                    {
                        'Key': 'mlctl',
                        'Value': '0.0.1'
                    }
                ]
            )

            variants.append({
                'VariantName': 'main',
                'ModelName': model['name']+ '-model',
                'InitialInstanceCount': job_definition['infrastructure']['deploy']['resources']['instance_count'],
                'InstanceType': job_definition['infrastructure']['deploy']['resources']['instance_type'],
                'InitialVariantWeight': model['traffic'],
            })

        print(response)

        response = self.client.create_endpoint_config(
            EndpointConfigName=job_definition['name']+ '-endpoint-config',
            ProductionVariants= variants,
            # DataCaptureConfig={
            #     'EnableCapture': True|False,
            #     'InitialSamplingPercentage': 123,
            #     'DestinationS3Uri': 'string',
            #     'KmsKeyId': 'string',
            #     'CaptureOptions': [
            #         {
            #             'CaptureMode': 'Input'|'Output'
            #         },
            #     ],
            #     'CaptureContentTypeHeader': {
            #         'CsvContentTypes': [
            #             'string',
            #         ],
            #         'JsonContentTypes': [
            #             'string',
            #         ]
            #     }
            # },
            Tags=[
                {
                    'Key': 'mlctl',
                    'Value': 'asdf'
                },
            ],
        )

    def start_deploy(self, job):
        job_definition = job.serialize()
        response = self.client.create_endpoint(
            EndpointName=job_definition['name'] + '-endpoint',
            EndpointConfigName=job_definition['name'] + '-endpoint-config',
            Tags=[
                {
                    'Key': 'mlctl',
                    'Value': '0.0.1'
                },
            ]
        )

        print(response)


    def get_deploy_info(self, job):
        pass

    def stop_deploy(self, job):
        try:
            pass
        except Exception as e:
            return str(e)
