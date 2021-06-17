from abc import ABC, abstractmethod


class Training(ABC):
    @abstractmethod
    def start_training(self, training_job_config, hyperparameter_tuning):
        pass

    @abstractmethod
    def get_training_info(self, training_job_name, hyperparameter_tuning):
        pass

    @abstractmethod
    def stop_training(self, training_job_name, hyperparameter_tuning):
        pass
