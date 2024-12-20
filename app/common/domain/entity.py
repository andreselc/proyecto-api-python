from abc import ABC, abstractmethod

class Entity(ABC):
    @abstractmethod
    def get(self):
        pass