from app.common.domain.value_object import ValueObject

class Description(ValueObject):
    def __init__(self, description: str):
        self._description = description

    @classmethod
    def create(cls, description: str):
        return cls(description)

    def get(self) -> str:
        return self._description