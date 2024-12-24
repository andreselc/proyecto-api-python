from app.common.domain.value_object import ValueObject

class Code(ValueObject):
    def __init__(self, code: str):
        self._code = code

    @classmethod
    def create(cls, code: str):
        return cls(code)

    def get(self) -> str:
        return self._code