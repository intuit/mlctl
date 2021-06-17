from mlctl.interfaces.Training import Training
from mlctl.plugins.utils import parse_config
import boto3


class SagemakerTraining(Training):

    def __init__(self, profile=None):
        if profile:
            boto3.setup_default_session(profile_name=profile)
        self._client = boto3.client("sagemaker")

    def start_training(self, config, hyperparameter_tuning=False):
        try:
            if hyperparameter_tuning == True:
                parameters = ["HyperParameterTuningJobName",
                              "HyperParameterTuningJobConfig",
                              "TrainingJobDefinition",
                              "TrainingJobDefinitions",
                              "WarmStartConfig",
                              "Tags"]
                kwargs = parse_config(config, parameters)
                return self._client.create_hyper_parameter_tuning_job(
                    **{k: v for k, v in kwargs.items() if v is not None})

            else:
                parameters = ["TrainingJobName",
                              "HyperParameters",
                              "AlgorithmSpecification",
                              "RoleArn",
                              "InputDataConfig",
                              "OutputDataConfig",
                              "ResourceConfig",
                              "VpcConfig",
                              "StoppingCondition",
                              "Tags",
                              "EnableNetworkIsolation",
                              "EnableInterContainerTrafficEncryption",
                              "EnableManagedSpotTraining",
                              "CheckpointConfig",
                              "DebugHookConfig",
                              "DebugRuleConfigurations",
                              "TensorBoardOutputConfig",
                              "ExperimentConfig",
                              "ProfilerConfig",
                              "ProfilerRuleConfigurations",
                              "Environment"]
                kwargs = parse_config(config, parameters)
                return self._client.create_training_job(
                    **{k: v for k, v in kwargs.items() if v is not None}
                )
        except Exception as e:
            return str(e)

    def get_training_info(self, training_job_name, hyperparameter_tuning=False):
        try:
            if hyperparameter_tuning:
                return self._client.describe_hyper_parameter_tuning_job(
                    HyperParameterTuningJobName=training_job_name)
            else:
                return self._client.describe_training_job(
                    TrainingJobName=training_job_name)
        except Exception as e:
            return str(e)

    def stop_training(self, training_job_name, hyperparameter_tuning=False):
        try:
            if hyperparameter_tuning:
                return self._client.stop_hyper_parameter_tuning_job(
                    HyperParameterTuningJobName=training_job_name)
            else:
                return self._client.stop_training_job(
                    TrainingJobName=training_job_name)
        except Exception as e:
            return str(e)
