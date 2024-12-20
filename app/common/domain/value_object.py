from abc import ABC, abstractmethod

class ValueObject(ABC):
    @classmethod
    @abstractmethod
    def create(cls, value: str):
        pass

    @abstractmethod
    def get(self) -> str:
        pass