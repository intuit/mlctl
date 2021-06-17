from abc import ABC, abstractmethod


class Hosting(ABC):
    @abstractmethod
    def create(self, model_config):
        pass

    @abstractmethod
    def deploy(self, endpoint_name, config):
        pass

    @abstractmethod
    def undeploy(self, endpoint_name):
        pass

    @abstractmethod
    def get_endpoint_info(self, endpoint_name):
        pass
