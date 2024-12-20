from app.products.domain.entities.product import Product
from app.products.domain.services.calculate_price import calculate_price

class ProductAggregate:
    def __init__(self, product: Product):
        self.product = product

    @classmethod
    def create(cls, name: str, code: str, description: str, margin_profit: float, cost: float, status: str):
        price = calculate_price(cost, margin_profit)
        product = Product.create(name, code, description, price, margin_profit, cost, status)
        return cls(product)

    def update(self, name: str = None, code: str = None, description: str = None, margin_profit: float = None, cost: float = None, status: str = None):
        if margin_profit is not None and cost is not None:
            price = calculate_price(cost, margin_profit)
            self.product.update(name, code, description, price, margin_profit, cost, status)
        else:
            self.product.update(name, code, description, None, margin_profit, cost, status)