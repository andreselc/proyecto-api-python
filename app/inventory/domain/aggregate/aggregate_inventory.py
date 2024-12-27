from app.products.domain.services.calculate_price import calculate_price
from app.products.domain.entities.product import Product
from app.inventory.domain.entities.inventory import Inventory
from app.inventory.domain.value_objects.id import ID
from app.common.domain.entity import Entity

class InventoryAggregate(Entity):
    def __init__(self, id: ID, inventory: Inventory, product: Product):
        self.id = id
        self.inventory = inventory
        self.product = product

    @classmethod
    def create(cls, quantity: int, product_id: str,  name: str, code: str, description: str, margin_profit: float, cost: float, status: str):
        id = ID.create()
        inventory = Inventory.create(quantity)
        price = calculate_price(cost, margin_profit)
        product = Product.create(product_id, name, code, description, price, margin_profit, cost, status)
        return cls(id, inventory, product)
    
    def update(self, quantity: int = None, name: str = None, code: str = None, description: str = None, margin_profit: float = None, cost: float = None, status: str = None):
        if quantity is not None:
            self.inventory.update(quantity)
        if margin_profit is not None and cost is not None:
            price = calculate_price(cost, margin_profit)
            self.product.update(name, code, description, price, margin_profit, cost, status)
        else:
            self.product.update(name, code, description, None, margin_profit, cost, status)

    def get(self):
        return self.inventory, self.product
    
