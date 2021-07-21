from mlctl.plugins.sagemaker.SagemakerBatch import SagemakerBatch
from mlctl.plugins.sagemaker.SagemakerHosting import SagemakerHosting
from mlctl.plugins.sagemaker.SagemakerTraining import SagemakerTraining
from mlctl.plugins.azureml.AzureMlTraining import AzureMlTraining


def determine_plugin(plugin, profile, capability):
    if plugin == 'sagemaker':
        if capability == 'batch':
            return SagemakerBatch(profile)
        elif capability == 'hosting':
            return SagemakerHosting(profile)
        elif capability == 'training':
            return SagemakerTraining(profile)
        else:
            print(f'{capability} is not a valid job')
    elif plugin == 'azureml':
        if capability == 'training':
            return AzureMlTraining(profile)