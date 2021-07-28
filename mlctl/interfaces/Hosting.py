from abc import ABC, abstractmethod


class Hosting(ABC):
    @abstractmethod
    def create(self, job):
        pass

    @abstractmethod
    def start_hosting(self, job):
        pass

    @abstractmethod
    def stop_hosting(self, job):
        pass

    @abstractmethod
    def get_hosting_info(self, job):
        pass
