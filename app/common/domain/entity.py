from abc import ABC, abstractmethod

class Entity(ABC):
    @abstractmethod
    def get(self):
        pass

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass