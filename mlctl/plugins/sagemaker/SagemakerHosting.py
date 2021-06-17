from mlctl.interfaces.Hosting import Hosting
from mlctl.plugins.utils import parse_config
import boto3


class SagemakerHosting(Hosting):
    def __init__(self, profile=None):
        if profile:
            boto3.setup_default_session(profile_name=profile)
        self._client = boto3.client("sagemaker")

    def create(self, model_config):
        try:
            kwargs = parse_config(model_config, ["ModelName",
                                                 "PrimaryContainer",
                                                 "Container",
                                                 "InferenceExecutionConfig",
                                                 "ExecutionRoleArn",
                                                 "Tags",
                                                 "VpcConfig",
                                                 "EnableNetworkIsolation"])
            return self._client.create_model(**{k: v for k, v in kwargs.items() if v is not None})
        except Exception as e:
            return str(e)

    def deploy(self, endpoint_name, endpoint_config_name=None, endpoint_config=None, tags=None):
        config_name = endpoint_config_name
        try:
            if endpoint_config:
                kwargs = parse_config(endpoint_config, ["EndpointConfigName",
                                                        "ProductionVariants",
                                                        "DataCaptureConfig",
                                                        "Tags",
                                                        "KmsKeyId"])
                response = self._client.create_endpoint_config(
                    **{k: v for k, v in kwargs.items() if v is not None})
                print(response)
                config_name = kwargs.get("EndpointConfigName")
            if tags:
                return self._client.create_endpoint(
                    EndpointName=endpoint_name,
                    EndpointConfigName=config_name,
                    Tags=tags
                )
            else:
                return self._client.create_endpoint(
                    EndpointName=endpoint_name,
                    EndpointConfigName=config_name
                )
        except Exception as e:
            return str(e)

    def undeploy(self, endpoint_name, endpoint_config_name=None):
        message = "Successfully undeployed endpoint: " + endpoint_name
        try:
            self._client.delete_endpoint(EndpointName=endpoint_name)
            if endpoint_config_name:
                self._client.delete_endpoint_config(
                    EndpointConfigName=endpoint_config_name
                )
                message += "\nSuccessfully deleted endpoint config: " + endpoint_config_name
            return message
        except Exception as e:
            return str(e)

    def get_endpoint_info(self, endpoint_name):
        try:
            return self._client.describe_endpoint(EndpointName=endpoint_name)
        except Exception as e:
            return str(e)
