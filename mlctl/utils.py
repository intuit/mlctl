from mlctl.plugins.sagemaker.SagemakerBatch import SagemakerBatch
from mlctl.plugins.sagemaker.SagemakerHosting import SagemakerHosting
from mlctl.plugins.sagemaker.SagemakerTraining import SagemakerTraining


def determine_plugin(plugin, profile, capability):
    if plugin == 'sagemaker':
        if capability == 'batch':
            return SagemakerBatch(profile)
        if capability == 'hosting':
            return SagemakerHosting(profile)
        if capability == 'training':
            return SagemakerTraining(profile)
