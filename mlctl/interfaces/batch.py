from abc import ABC, abstractmethod


class Batch(ABC):
    @abstractmethod
    def start_batch(self, batch_job_config):
        pass

    @abstractmethod
    def get_batch_info(self, batch_job_name):
        pass

    @abstractmethod
    def stop_batch(self, batch_job_name):
        pass
