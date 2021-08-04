from abc import ABC, abstractmethod


class Processing(ABC):
    @abstractmethod
    def start_processing(self, training_job_config, hyperparameter_tuning):
        pass

    @abstractmethod
    def get_processing_info(self, training_job_name, hyperparameter_tuning):
        pass

    @abstractmethod
    def stop_processing(self, training_job_name, hyperparameter_tuning):
        pass
