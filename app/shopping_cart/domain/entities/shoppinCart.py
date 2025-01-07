from app.common.domain.entity import Entity
from app.shopping_cart.domain.value_objects.id import ID
from app.shopping_cart.domain.value_objects.quantity import Quantity

class ShoppinCart(Entity):
    def __init__(self, id: ID, quantity: Quantity):
        self.id = id
        self.quantity = quantity

    @classmethod
    def create(cls, id: str ,quantity: int):
        id = ID.create(id)
        quantity = Quantity.create(quantity)
        return cls(id, quantity)
    
    def update(self, quantity: int):
        if quantity:
            self.quantity = Quantity.create(quantity)

    def get(self):
        return self