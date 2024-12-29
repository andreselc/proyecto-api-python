from app.common.domain.entity import Entity
from app.shopping_cart.domain.entities.shoppinCart import ShoppinCart
from app.shopping_cart.domain.value_objects.id import ID
from app.products.domain.entities.product import Product
from app.users.domain.entities.user import User
from app.products.domain.services.calculate_price import calculate_price

class ShoppinCartAggregate(Entity):
    def __init__(self, id: ID, shoppin_cart: ShoppinCart, product: Product, user: User):
        self.id = id
        self.shoppin_cart = shoppin_cart
        self.product = product
        self.user = user

    @classmethod
    def create(cls, quantity: int, product_id: str, name: str, code: str, description: str, margin_profit: float, cost: float, status: str, user_id: str ,user_name: str, username: str, email: str, password: str, role: str):
        id = ID.create()
        shoppin_cart = ShoppinCart.create(quantity)
        price = calculate_price(cost, margin_profit)
        product = Product.create(product_id, name, code, description, price, margin_profit, cost, status)
        user = User.create(user_id, user_name, username, email, password, role)
        return cls(id, shoppin_cart, product, user)
    
    def update(self, quantity: int = None):
        if quantity is not None:
            self.shoppin_cart.update(quantity)

    def get(self):
        return self.shoppin_cart, self.product, self.user