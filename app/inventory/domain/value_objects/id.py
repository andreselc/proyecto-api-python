from uuid import uuid4
from app.common.domain.value_object import ValueObject

class ID(ValueObject):
    def __init__(self, id: str):
        self._id = id

    @classmethod
    def create(cls):
        return cls(str(uuid4()))

    def get(self) -> str:
        return self._id