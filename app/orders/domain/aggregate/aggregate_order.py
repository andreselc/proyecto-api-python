from app.common.domain.entity import Entity
from app.orders.domain.entities.order import Order
from app.orders.domain.value_objects.id import ID
from app.products.domain.entities.product import Product
from app.users.domain.entities.user import User
from app.orders.domain.services.calculate_total_price import calculate_total_price

class OrderAggregate(Entity):
    def __init__(self, id: ID, order: Order, products: list[Product], user: User):
        self.id = id
        self.order = order
        self.products = products
        self.user = user

    @classmethod
    def create(cls, id: str, status: str, products: list[Product], user_id: str, user_name: str, username: str, email: str, password: str, role: str):
        totalprice = calculate_total_price(products)
        order = Order.create(id, totalprice, status)
        user = User.create(user_id, user_name, username, email, password, role)
        return cls(id, order, products, user)
    
    def update(self, totalprice: float = None, status: str = None):
        if totalprice:
            self.order.update(totalprice)
        if status:
            self.order.update(status)

    def get(self):
        return self.order, self.products, self.user



