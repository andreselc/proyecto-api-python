from app.common.domain.entity import Entity
from app.orders.domain.value_objects.id import ID
from app.orders.domain.value_objects.totalprice import TotalPrice
from app.orders.domain.enums.status import Status

class Order(Entity): 
    def __init__(self, id: ID, totalprice: TotalPrice, status: Status):
        self.id = id
        self.totalprice = totalprice
        self.status = status

    @classmethod
    def create(cls, id: str, totalprice: float, status: str):
        id = ID.create(id)
        totalprice = TotalPrice.create(totalprice)
        status = Status[status.upper()]
        return cls(id, totalprice, status)

    def update(self, totalprice: float = None, status: str = None):
        if totalprice:
            self.totalprice = TotalPrice.create(totalprice)
        if status:
            self.status = Status[status.upper()]

    def get(self):
        return self