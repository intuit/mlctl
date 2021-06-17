from unittest import mock
import unittest
import datetime
from mlctl.plugins.sagemaker.SagemakerBatch import SagemakerBatch
import boto3
from botocore.stub import Stubber
import botocore.session
import json


class TestSagemakerBatch(unittest.TestCase):

    def setUp(self):
        self._transform_job_arn = "arn:aws:sagemaker:us-west-2:123456789098:transform-job/test-batch"
        config_content = {
            "ModelName": "test-model",
            "TransformInput": {
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": "s3://test-bucket/input/"
                    }
                }
            },
            "TransformJobName": "test-transform-job",
            "TransformOutput": {
                "KmsKeyId": "arn:aws:kms:us-west-2:123456789098:key/key",
                "S3OutputPath": "s3://test-bucket/output/"
            },
            "TransformResources": {
                "InstanceCount": 1,
                "InstanceType": "ml.m5.large",
                "VolumeKmsKeyId": "arn:aws:kms:us-west-2:123456789098:key/key"
            }
        }
        self._mock_config = json.dumps(config_content)

    @mock.patch.object(boto3, 'client')
    def test_start(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response('create_transform_job',
                             {
                                 "TransformJobArn": self._transform_job_arn,
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        with mock.patch('builtins.open', new_callable=mock.mock_open, read_data=self._mock_config):
            sagemaker_batch = SagemakerBatch()
            response = sagemaker_batch.start_batch("batch_config.json")
            self.assertEqual(
                self._transform_job_arn, response["TransformJobArn"])

    @mock.patch.object(boto3, 'client')
    def test_start_throws_exception(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_client_error('create_transform_job', "ValidationException",
                                 "Could not find model \"arn:aws:sagemaker:us-west-2:123456789098:model/test-model\".")
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        with mock.patch('builtins.open', new_callable=mock.mock_open, read_data=self._mock_config):
            sagemaker_batch = SagemakerBatch()
            response = sagemaker_batch.start_batch("batch_config.json")
            self.assertEqual(
                "An error occurred (ValidationException) when calling the CreateTransformJob operation: Could not find model \"arn:aws:sagemaker:us-west-2:123456789098:model/test-model\".", response)

    @mock.patch.object(boto3, 'client')
    def test_get_batch_info(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response('describe_transform_job',
                             {
                                 "TransformJobName": "test-transform-job",
                                 "TransformJobArn": self._transform_job_arn,
                                 "TransformJobStatus": "Stopped",
                                 "ModelName": "test-model",
                                 "TransformInput": {
                                     "DataSource": {
                                         "S3DataSource": {
                                             "S3DataType": "S3Prefix",
                                             "S3Uri": "s3://test-bucket/input/"
                                         }
                                     }
                                 },
                                 "TransformOutput": {
                                     "S3OutputPath": "s3://test-model/output/",
                                     "KmsKeyId": "arn:aws:kms:us-west-2:123456789098:key/key"
                                 },
                                 "TransformResources": {
                                     "InstanceType": "ml.m5.large",
                                     "InstanceCount": 1,
                                     "VolumeKmsKeyId": "arn:aws:kms:us-west-2:123456789098:key/key"
                                 },
                                 "CreationTime": datetime.datetime.now()
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_batch = SagemakerBatch()
        response = sagemaker_batch.get_batch_info("test-transform-job")
        self.assertEqual(self._transform_job_arn, response["TransformJobArn"])

    @mock.patch.object(boto3, "client")
    def test_get_batch_info_throws_exception(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_client_error('describe_transform_job', "ExpiredTokenException",
                                 "The security token included in the request is expired")
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_batch = SagemakerBatch()
        response = sagemaker_batch.get_batch_info("test-transform-job")
        self.assertEqual(
            "An error occurred (ExpiredTokenException) when calling the DescribeTransformJob operation: The security token included in the request is expired", response)

    @mock.patch.object(boto3, 'client')
    def test_stop(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response('stop_transform_job',
                             {
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_batch = SagemakerBatch()
        response = sagemaker_batch.stop_batch("test-transform-job")
        self.assertEqual(200, response["ResponseMetadata"]["HTTPStatusCode"])

    @mock.patch.object(boto3, "client")
    def test_stop_throws_exception(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_client_error('stop_transform_job', "ValidationException",
                                 "The request was rejected because the transform job is in status Stopped")
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_batch = SagemakerBatch()
        response = sagemaker_batch.stop_batch("test-transform-job")
        self.assertEqual(
            "An error occurred (ValidationException) when calling the StopTransformJob operation: The request was rejected because the transform job is in status Stopped", response)

    def test_set_profile(self):
        with self.assertRaises(botocore.exceptions.ProfileNotFound) as context:
            SagemakerBatch("nonExistantProfile")

        self.assertEqual(
            'The config profile (nonExistantProfile) could not be found', str(context.exception))
