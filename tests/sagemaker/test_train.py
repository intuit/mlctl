from unittest import mock
import unittest
import datetime
from mlctl.plugins.sagemaker.SagemakerTraining import SagemakerTraining
import boto3
from botocore.stub import Stubber
import botocore.session
import json
import botocore


class TestSagemakerTrain(unittest.TestCase):

    def setUp(self):
        config_content = {
            "AlgorithmSpecification": {
                "TrainingImage": "433757028032.dkr.ecr.us-west-2.amazonaws.com/xgboost:1",
                "TrainingInputMode": "File"
            },
            "EnableInterContainerTrafficEncryption": True,
            "EnableNetworkIsolation": True,
            "HyperParameters": {
                "max_depth": "5",
                "eta": "0.2",
                "gamma": "4",
                "min_child_weight": "6",
                "subsample": "0.8",
                "silent": "0",
                "objective": "binary:logistic",
                "num_round": "100"
            },
            "InputDataConfig": [
                {
                    "ChannelName": "train",
                    "ContentType": "csv",
                    "DataSource": {
                        "S3DataSource": {
                            "S3DataType": "S3Prefix",
                            "S3Uri": "s3://test-bucket/input/"
                        }
                    }
                }
            ],
            "OutputDataConfig": {
                "KmsKeyId": "arn:aws:kms:us-west-2:123456789098:key/key",
                "S3OutputPath": "s3://test-bucket/output/"
            },
            "ResourceConfig": {
                "InstanceCount": 1,
                "InstanceType": "ml.m5.xlarge",
                "VolumeKmsKeyId": "arn:aws:kms:us-west-2:123456789098:key/key",
                "VolumeSizeInGB": 1
            },
            "RoleArn": "arn:aws:iam::123456789098:role/test-role",
            "StoppingCondition": {
                "MaxRuntimeInSeconds": 86400
            },
            "TrainingJobName": "test-training-job"
        }
        self._mock_config = json.dumps(config_content)
        self._training_job_arn = "arn:aws:sagemaker:us-west-2:123456789098:training-job/test-training-job"

    @mock.patch.object(boto3, 'client')
    def test_start(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response('create_training_job',
                             {
                                 "TrainingJobArn": self._training_job_arn,
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        with mock.patch('builtins.open', new_callable=mock.mock_open, read_data=self._mock_config):
            sagemaker_train = SagemakerTraining()
            response = sagemaker_train.start_training("training_config.json")
            self.assertEqual(
                self._training_job_arn, response["TrainingJobArn"])

    @mock.patch.object(boto3, 'client')
    def test_start_throws_exception(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_client_error("create_hyper_parameter_tuning_job")
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        with mock.patch('builtins.open', new_callable=mock.mock_open, read_data="{}"):
            sagemaker_train = SagemakerTraining()
            response = sagemaker_train.start_training(
                "hyperparameter_tuning_config.json", True)
            self.assertEqual(
                "Parameter validation failed:\nMissing required parameter in input: \"HyperParameterTuningJobName\"\nMissing required parameter in input: \"HyperParameterTuningJobConfig\"", response)

    @mock.patch.object(boto3, 'client')
    def test_get_training_info(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response('describe_training_job',
                             {
                                 "TrainingJobName": "test-training-job",
                                 "TrainingJobArn": self._training_job_arn,
                                 "ModelArtifacts": {
                                     "S3ModelArtifacts": 's3://test-bucket/output/test-training-job/output/model.tar.gz'
                                 },
                                 "TrainingJobStatus": "Completed",
                                 "SecondaryStatus": "Completed",
                                 "AlgorithmSpecification": {
                                     "TrainingInputMode": "File"
                                 },
                                 "ResourceConfig": {
                                     "InstanceType": "ml.m5.xlarge",
                                     "InstanceCount": 1,
                                     "VolumeSizeInGB": 1
                                 },
                                 "StoppingCondition": {
                                     'MaxRuntimeInSeconds': 86400
                                 },
                                 "CreationTime": datetime.datetime.now()
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_train = SagemakerTraining()
        response = sagemaker_train.get_training_info("test-training-job")
        self.assertEqual(
            self._training_job_arn, response["TrainingJobArn"])

    @mock.patch.object(boto3, 'client')
    def test_get_hyperparameter_tuning_status(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response('describe_hyper_parameter_tuning_job',
                             {
                                 "HyperParameterTuningJobName": "test-tuning-job",
                                 "HyperParameterTuningJobArn": "arn:aws:sagemaker:us-west-2:123456789098:hyper-parameter-tuning-job/test-tuning-job",
                                 "HyperParameterTuningJobConfig": {
                                     "Strategy": "Bayesian",
                                     "ResourceLimits": {
                                         "MaxNumberOfTrainingJobs": 1,
                                         "MaxParallelTrainingJobs": 1
                                     }
                                 },
                                 "HyperParameterTuningJobStatus": "InProgress",
                                 "CreationTime": datetime.datetime.now(),
                                 "TrainingJobStatusCounters": {
                                     "Completed": 0,
                                     "InProgress": 1,
                                     "RetryableError": 0,
                                     "NonRetryableError": 0,
                                     "Stopped": 0
                                 },
                                 "ObjectiveStatusCounters": {
                                     "Succeeded": 0,
                                     "Pending": 1,
                                     "Failed": 0
                                 }
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_train = SagemakerTraining()
        response = sagemaker_train.get_training_info("test-training-job", True)
        self.assertEqual(
            "arn:aws:sagemaker:us-west-2:123456789098:hyper-parameter-tuning-job/test-tuning-job", response["HyperParameterTuningJobArn"])

    @mock.patch.object(boto3, 'client')
    def test_get_training_info_throws_exception(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_client_error(
            'describe_training_job', "ValidationException", "Requested resource not found.")
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_train = SagemakerTraining()
        response = sagemaker_train.get_training_info("test-training-job")
        self.assertEqual(
            "An error occurred (ValidationException) when calling the DescribeTrainingJob operation: Requested resource not found.", response)

    @mock.patch.object(boto3, 'client')
    def test_stop(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response('stop_training_job',
                             {
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_train = SagemakerTraining()
        response = sagemaker_train.stop_training("test-training-job")
        self.assertEqual(200, response["ResponseMetadata"]["HTTPStatusCode"])

    @mock.patch.object(boto3, 'client')
    def test_stop_hyperparameter_tuning(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_response('stop_hyper_parameter_tuning_job',
                             {
                                 "ResponseMetadata": {
                                     "HTTPStatusCode": 200,
                                     "RetryAttempts": 0
                                 }
                             })
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_train = SagemakerTraining()
        response = sagemaker_train.stop_training(
            "test-hyperparameter-tuning-training-job", True)
        self.assertEqual(200, response["ResponseMetadata"]["HTTPStatusCode"])

    @mock.patch.object(boto3, 'client')
    def test_stop_throws_exception(self, mock_boto_client):
        stubbed_client = botocore.session.get_session().create_client('sagemaker')
        stubber = Stubber(stubbed_client)
        stubber.add_client_error(
            'stop_training_job', "ValidationException", "Requested resource not found.")
        stubber.activate()
        mock_boto_client.return_value = stubbed_client

        sagemaker_train = SagemakerTraining()
        response = sagemaker_train.stop_training("test-training-job")
        self.assertEqual(
            "An error occurred (ValidationException) when calling the StopTrainingJob operation: Requested resource not found.", response)

    def test_set_profile(self):
        with self.assertRaises(botocore.exceptions.ProfileNotFound) as context:
            SagemakerTraining("nonExistantProfile")

        self.assertEqual(
            'The config profile (nonExistantProfile) could not be found', str(context.exception))
