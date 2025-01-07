from app.common.infrastructure.Modelo import OrderModel, ProductModel, User
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.orders.domain.entities.order import Order
from app.orders.domain.value_objects.id import ID
from app.orders.domain.value_objects.totalprice import TotalPrice
from app.orders.domain.enums.status import Status
from app.products.domain.entities.product import Product
from app.products.domain.value_objects.id import ID as ProductID
from app.products.domain.value_objects.name import Name
from app.products.domain.value_objects.description import Description
from app.products.domain.value_objects.code import Code
from app.products.domain.value_objects.price import Price
from app.products.domain.value_objects.margin_profit import MarginProfit
from app.products.domain.value_objects.cost import Cost
from app.products.domain.enums.status import Status as ProductStatus
from app.users.domain.entities.user import User
from app.users.domain.value_object.id import Id as UserID
from app.users.domain.value_object.name import Name as UserName
from app.users.domain.value_object.email import Email
from app.users.domain.value_object.password import Password
from app.users.domain.value_object.username import Username
from app.users.domain.enums.roleEnum import Role

def model_to_domain(order_model: OrderModel, product_models: list[ProductModel], user_model: User) -> OrderAggregate:
    order = Order(
        id=ID(order_model.id),
        totalprice=TotalPrice(order_model.total_price),
        status=Status(order_model.status)
    )
    
    products = [
        Product(
            id=ProductID(product_model.id),
            name=Name(product_model.name),
            code=Code(product_model.code),
            description=Description(product_model.description),
            price=Price(product_model.price),
            margin_profit=MarginProfit(product_model.profit_margin),
            cost=Cost(product_model.cost),
            status=ProductStatus(product_model.status)
        )
        for product_model in product_models
    ]
    
    user = User(
        id=UserID(user_model.id),
        name=UserName(user_model.name),
        email=Email(user_model.email),
        username=Username(user_model.username),
        password=Password(user_model.password),
        role=Role(user_model.role)
    )
    
    return OrderAggregate(id=ID(order_model.id), order=order, products=products, user=user)