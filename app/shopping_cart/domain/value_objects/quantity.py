from app.common.domain.value_object import ValueObject

class Quantity(ValueObject):
    def __init__(self, quantity: int):
        self._quantity = quantity

    @classmethod
    def create(cls, quantity: int):
        return cls(quantity)

    def get(self) -> int:
        return self._quantity