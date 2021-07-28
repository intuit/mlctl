import yaml
from pathlib import Path
import boto3
from distutils.core import run_setup

from mlctl.interfaces.Hosting import Hosting
from mlctl.plugins.utils import parse_config, run_subprocess


class AwsSagemakerHosting(Hosting):
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
                    'Image': job_definition['infrastructure']['hosting']['container_repo'] + ':predict-image',
                    'ImageConfig': {
                        'RepositoryAccessMode': 'Platform',
                    },
                    'Mode': 'SingleModel',
                    'ModelDataUrl': model['artifact'],
                    'Environment': {
                        'sriracha_provider': 'awssagemaker'
                    },
                },
                ExecutionRoleArn= job_definition['infrastructure']['hosting']['arn'],
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
                'InitialInstanceCount': job_definition['infrastructure']['hosting']['resources']['instance_count'],
                'InstanceType': job_definition['infrastructure']['hosting']['resources']['instance_type'],
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

    def start_hosting(self, job):
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


    def get_hosting_info(self, job):
        pass

    def stop_hosting(self, job):
        try:
            pass
        except Exception as e:
            return str(e)
