from app.products.domain.entities.product import Product
from app.products.domain.services.calculate_price import calculate_price
from app.common.domain.entity import Entity
from app.products.domain.value_objects.id import ID

class ProductAggregate(Entity):
    def __init__(self, id: ID, product: Product):
        self.id = id
        self.product = product

    @classmethod
    def create(cls, id: str, name: str, code: str, description: str, margin_profit: float, cost: float, status: str):
        price = calculate_price(cost, margin_profit)
        product = Product.create(id, name, code, description, price, margin_profit, cost, status)
        return cls(id, product)

    def update(self, name: str = None, code: str = None, description: str = None, margin_profit: float = None, cost: float = None, status: str = None):
        if margin_profit is not None and cost is not None:
            price = calculate_price(cost, margin_profit)
            self.product.update(name, code, description, price, margin_profit, cost, status)
        else:
            self.product.update(name, code, description, None, margin_profit, cost, status)

    def get(self):
        return self.product