from app.common.domain.value_object import ValueObject

class TotalPrice(ValueObject):
    def __init__(self, totalprice: float):
        self._totalprice = totalprice

    @classmethod
    def create(cls, totalprice: float):
        return cls(totalprice)

    def get(self) -> float:
        return self._totalprice