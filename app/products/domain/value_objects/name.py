from app.common.domain.value_object import ValueObject

class Name(ValueObject):
    def __init__(self, name: str):
        self._name = name

    @classmethod
    def create(cls, name: str):
        return cls(name)

    def get(self) -> str:
        return self._name