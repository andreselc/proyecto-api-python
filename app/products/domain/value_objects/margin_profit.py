from app.common.domain.value_object import ValueObject

class MarginProfit(ValueObject):
    def __init__(self, margin_profit: float):
        self._margin_profit = margin_profit

    @classmethod
    def create(cls, margin_profit: float):
        return cls(margin_profit)

    def get(self) -> float:
        return self._margin_profit