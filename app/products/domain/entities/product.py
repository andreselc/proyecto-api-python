from app.products.domain.value_objects.id import ID
from app.products.domain.value_objects.name import Name
from app.products.domain.value_objects.description import Description
from app.products.domain.value_objects.code import Code
from app.products.domain.value_objects.price import Price
from app.products.domain.value_objects.margin_profit import MarginProfit
from app.products.domain.value_objects.cost import Cost
from app.products.domain.enums.status import Status
from app.common.domain.entity import Entity

class Product(Entity):
    def __init__(self, id: ID, name: Name, code: Code, description: Description, price: Price, margin_profit: MarginProfit, cost: Cost, status: Status):
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.price = price
        self.margin_profit = margin_profit
        self.cost = cost
        self.status = status

    @classmethod
    def create(cls, name: str, code: str, description: str, price: float, margin_profit: float, cost: float, status: str):
        id = ID.create()
        name = Name.create(name)
        code = Code.create(code)
        description = Description.create(description)
        price = Price.create(price)
        margin_profit = MarginProfit.create(margin_profit)
        cost = Cost.create(cost)
        status = Status[status.upper()]
        return cls(id, name, code, description, price, margin_profit, cost, status)

    def update(self, name: str = None, code: str = None, description: str = None, price: float = None, margin_profit: float = None, cost: float = None, status: str = None):
        if name:
            self.name = Name.create(name)
        if code:
            self.code = Code.create(code)
        if description:
            self.description = Description.create(description)
        if price:
            self.price = Price.create(price)
        if margin_profit:
            self.margin_profit = MarginProfit.create(margin_profit)
        if cost:
            self.cost = Cost.create(cost)
        if status:
            self.status = Status[status.upper()]

    def get(self):
        return self