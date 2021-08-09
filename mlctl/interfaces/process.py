from abc import ABC, abstractmethod


class Process(ABC):
    @abstractmethod
    def start_process(self, processing_job_config):
        pass

    @abstractmethod
    def get_process_info(self, processing_job_name):
        pass

    @abstractmethod
    def stop_process(self, processing_job_name):
        pass
