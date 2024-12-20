from app.common.domain.value_object import ValueObject

class Price(ValueObject):
    def __init__(self, price: float):
        self._price = price

    @classmethod
    def create(cls, price: float):
        return cls(price)

    def get(self) -> float:
        return self._price