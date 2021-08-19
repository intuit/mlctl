from abc import ABC, abstractmethod


class Deploy(ABC):
    @abstractmethod
    def create(self, job):
        pass

    @abstractmethod
    def start_deploy(self, job):
        pass

    @abstractmethod
    def stop_deploy(self, job):
        pass

    @abstractmethod
    def get_deploy_info(self, job):
        pass
