from mlctl.interfaces.Batch import Batch
from mlctl.plugins.utils import parse_config
import boto3


class SagemakerBatch(Batch):

    def __init__(self, profile=None):
        if profile:
            boto3.setup_default_session(profile_name=profile)
        self._client = boto3.client("sagemaker")

    def start_batch(self, config):
        try:
            kwargs = parse_config(config, ["TransformJobName",
                                           "ModelName",
                                           "MaxConcurrentTransforms",
                                           "ModelClientConfig",
                                           "MaxPayloadInMB",
                                           "BatchStrategy",
                                           "Environment",
                                           "TransformInput",
                                           "TransformOutput",
                                           "TransformResources",
                                           "DataProcessing",
                                           "Tags",
                                           "ExperimentConfig"])
            return self._client.create_transform_job(**{k: v for k, v in kwargs.items() if v is not None})
        except Exception as e:
            return str(e)

    def get_batch_info(self, batch_job_name):
        try:
            return self._client.describe_transform_job(TransformJobName=batch_job_name)
        except Exception as e:
            return str(e)

    def stop_batch(self, batch_job_name):
        try:
            return self._client.stop_transform_job(TransformJobName=batch_job_name)
        except Exception as e:
            return str(e)
