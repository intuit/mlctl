from unittest import mock
import unittest
import datetime
from mlctl.plugins.sagemaker.SagemakerHosting import SagemakerHosting
import boto3
from botocore.stub import Stubber
import botocore.session
import json
import botocore


class TestSagemakerHosting(unittest.TestCase):

    def setUp(self):
        self._model_arn = "arn:aws:sagemaker:us-west-2:123456789098:model/test-model"
        self._endpoint_arn = "arn:aws:sagemaker:us-west-2:123456789098:endpoint/test-endpoint"
        model_config_content = {
            "ModelName": "test-model",
            "PrimaryContainer": {
                "Image": "433757028032.dkr.ecr.us-west-2.amazonaws.com/xgboost:1",
                "ModelDataUrl": "s3://test-bucket/output/test-training-job/output/model.tar.gz"
            },
            "ExecutionRoleArn": "arn:aws:iam::123456789098:role/test-role"
        }
        self._mock_model_config = json.dumps(model_config_content)
        endpoint_config_content = {

            "EndpointConfigName": "test-endpoint-config",
            "KmsKeyId": "keyId",
            "ProductionVariants": [
                {
                    "InitialInstanceCount": 1,
                    "InitialVariantWeight": 1,
                    "InstanceType": "ml.m5.large",
                    "ModelName": "test-model",
                    "VariantName": "test-model-variant"
                }
            ]
        }
        self._mock_endpoint_config = json.dumps(endpoint_config_content)

    @mock.patch.object(boto3, 'client')
    def test_create(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response('create_model',
                             {
                                 "ModelArn": self._model_arn,
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        with mock.patch('builtins.open', new_callable=mock.mock_open, read_data=self._mock_model_config):
            sagemaker_hosting = SagemakerHosting()
            response = sagemaker_hosting.create("model_config.json")
            self.assertEqual(
                self._model_arn, response["ModelArn"])

    @mock.patch.object(boto3, 'client')
    def test_create_throws_exception(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_client_error("create_model", "ValidationError",
                                 "Cannot create already existing model \"arn:aws:sagemaker:us-west-2:123456789098:model/test-model\".")
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        with mock.patch('builtins.open', new_callable=mock.mock_open, read_data=self._mock_model_config):
            sagemaker_hosting = SagemakerHosting()
            response = sagemaker_hosting.create("model_config.json")
            self.assertEqual(
                "An error occurred (ValidationError) when calling the CreateModel operation: Cannot create already existing model \"arn:aws:sagemaker:us-west-2:123456789098:model/test-model\".", response)

    @mock.patch.object(boto3, 'client')
    def test_deploy_with_existing_config(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response("create_endpoint",
                             {
                                 "EndpointArn": self._endpoint_arn,
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_hosting = SagemakerHosting()
        response = sagemaker_hosting.deploy(
            "test-endpoint", "test-endpoint-config")
        self.assertEqual(
            self._endpoint_arn, response["EndpointArn"])

    @mock.patch.object(boto3, 'client')
    def test_deploy(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response('create_endpoint_config',
                             {
                                 "EndpointConfigArn": "arn:aws:sagemaker:us-west-2:123456789098:endpoint-config/test-endpoint-config",
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })
        stubber.add_response('create_endpoint',
                             {
                                 "EndpointArn": self._endpoint_arn,
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        with mock.patch('builtins.open', new_callable=mock.mock_open, read_data=self._mock_endpoint_config):
            sagemaker_hosting = SagemakerHosting()
            response = sagemaker_hosting.deploy(
                "test-endpoint", endpoint_config="endpoint_config.json", tags=[{"Key": "Environment", "Value": "testEnv"}])
            self.assertEqual(
                self._endpoint_arn, response["EndpointArn"])

    @mock.patch.object(boto3, 'client')
    def test_deploy_throws_exception(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_client_error('create_endpoint_config', "ValidationException",
                                 "Cannot create already existing endpoint configuration \"arn:aws:sagemaker:us-west-2:123456789098:endpoint-config/test-endpoint-config\".")
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        with mock.patch('builtins.open', new_callable=mock.mock_open, read_data=self._mock_endpoint_config):
            sagemaker_hosting = SagemakerHosting()
            response = sagemaker_hosting.deploy(
                "test-endpoint", endpoint_config="endpoint_config.json", tags=[{"Key": "Environment", "Value": "testEnv"}])
            self.assertEqual(
                "An error occurred (ValidationException) when calling the CreateEndpointConfig operation: Cannot create already existing endpoint configuration \"arn:aws:sagemaker:us-west-2:123456789098:endpoint-config/test-endpoint-config\".", response)

    @mock.patch.object(boto3, 'client')
    def test_undeploy(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response("delete_endpoint",
                             {
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_hosting = SagemakerHosting()
        response = sagemaker_hosting.undeploy("test-endpoint")
        self.assertEqual(
            "Successfully undeployed endpoint: test-endpoint", response)

    @mock.patch.object(boto3, 'client')
    def test_undeploy_delete_config(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response("delete_endpoint",
                             {
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })

        stubber.add_response("delete_endpoint_config",
                             {
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_hosting = SagemakerHosting()
        response = sagemaker_hosting.undeploy(
            "test-endpoint", "test-endpoint-config")
        self.assertEqual(
            "Successfully undeployed endpoint: test-endpoint\nSuccessfully deleted endpoint config: test-endpoint-config", response)

    @mock.patch.object(boto3, 'client')
    def test_undeploy_throws_exception(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_client_error("delete_endpoint", "ValidationException",
                                 "Cannot update in-progress endpoint \"arn:aws:sagemaker:us-west-2:123456789098:endpoint/test-endpoint\".")
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_hosting = SagemakerHosting()
        response = sagemaker_hosting.undeploy("test-endpoint")
        self.assertEqual("An error occurred (ValidationException) when calling the DeleteEndpoint operation: Cannot update in-progress endpoint \"arn:aws:sagemaker:us-west-2:123456789098:endpoint/test-endpoint\".", response)

    @mock.patch.object(boto3, 'client')
    def test_info(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response("describe_endpoint",
                             {
                                 "EndpointName": "test-endpoint",
                                 "EndpointArn": self._endpoint_arn,
                                 "EndpointConfigName": 'test-endpoint-config',
                                 "EndpointStatus": "InService",
                                 "CreationTime": datetime.datetime.now(),
                                 "LastModifiedTime": datetime.datetime.now()
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_hosting = SagemakerHosting()
        response = sagemaker_hosting.get_endpoint_info("test-endpoint")
        self.assertEqual(self._endpoint_arn, response["EndpointArn"])

    @mock.patch.object(boto3, 'client')
    def test_info_throws_exception(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_client_error("describe_endpoint", "ValidationException",
                                 "Could not find endpoint \"arn:aws:sagemaker:us-west-2:123456789098:endpoint/test-endpoint\".")
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_hosting = SagemakerHosting()
        response = sagemaker_hosting.get_endpoint_info("test-endpoint")
        self.assertEqual("An error occurred (ValidationException) when calling the DescribeEndpoint operation: Could not find endpoint \"arn:aws:sagemaker:us-west-2:123456789098:endpoint/test-endpoint\".", response)

    def test_set_profile(self):
        with self.assertRaises(botocore.exceptions.ProfileNotFound) as context:
            SagemakerHosting("nonExistantProfile")

        self.assertEqual(
            'The config profile (nonExistantProfile) could not be found', str(context.exception))
