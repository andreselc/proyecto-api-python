from app.common.domain.entity import Entity
from app.inventory.domain.value_objects.id import ID
from app.inventory.domain.value_objects.quantity import Quantity

class Inventory(Entity):
    def __init__(self, id: ID, quantity: Quantity):
        self.id = id
        self.quantity = quantity

    @classmethod
    def create(cls, quantity: int):
        id = ID.create()
        quantity = Quantity.create(quantity)
        return cls(id, quantity)

    def update(self, quantity: int):
        if quantity:
            self.quantity = Quantity.create(quantity)

    def get(self):
        return self