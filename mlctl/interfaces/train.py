from abc import ABC, abstractmethod


class Train(ABC):
    @abstractmethod
    def start_train(self, train_job_config, hyperparameter_tuning):
        pass

    @abstractmethod
    def get_train_info(self, train_job_name, hyperparameter_tuning):
        pass

    @abstractmethod
    def stop_train(self, train_job_name, hyperparameter_tuning):
        pass
