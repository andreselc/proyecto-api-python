from app.common.domain.value_object import ValueObject

class Cost(ValueObject):
    def __init__(self, cost: float):
        self._cost = cost

    @classmethod
    def create(cls, cost: float):
        return cls(cost)

    def get(self) -> float:
        return self._cost