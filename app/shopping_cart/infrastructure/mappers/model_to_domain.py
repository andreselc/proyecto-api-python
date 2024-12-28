from app.products.domain.value_objects.id import ID as ID_PRO
from app.products.domain.value_objects.name import Name as NAME_PRO
from app.products.domain.value_objects.description import Description
from app.products.domain.value_objects.code import Code
from app.products.domain.value_objects.price import Price
from app.products.domain.value_objects.margin_profit import MarginProfit
from app.products.domain.value_objects.cost import Cost
from app.products.domain.enums.status import Status
from app.products.domain.entities.product import Product

from app.users.domain.entities.user import User
from app.users.domain.value_object.id import Id
from app.users.domain.value_object.name import Name as NAME_USER
from app.users.domain.value_object.email import Email
from app.users.domain.value_object.password import Password
from app.users.domain.value_object.username import Username
from app.users.domain.enums.roleEnum import Role

from app.shopping_cart.domain.entities.shoppinCart import ShoppinCart
from app.shopping_cart.domain.value_objects.id import ID as ID_SHO
from app.shopping_cart.domain.value_objects.quantity import Quantity

from app.products.infrastructure.repository.productModel import ProductModel
from app.shopping_cart.infrastructure.model.shoppinCartModel import ShoppinCartModel
from app.users.infrastructure.model.ModelUser import User

from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate

def model_to_domain(shoppin_cart_model: ShoppinCartModel, product_model: ProductModel, user_model: User) -> ShoppinCartAggregate:
    shoppin_cart = ShoppinCart(
        id = ID_SHO(shoppin_cart_model.id),
        quantity = Quantity(shoppin_cart_model.quantity)
    )
    product = Product(
        id=ID_PRO(product_model.id),
        name=NAME_PRO(product_model.name),
        code=Code(product_model.code),
        description=Description(product_model.description),
        price=Price(product_model.price),
        margin_profit=MarginProfit(product_model.profit_margin),
        cost=Cost(product_model.cost),
        status=Status(product_model.status)
    )
    user = User(
        id = Id(user_model.id),
        name = NAME_USER(user_model.name),
        email=Email(user_model.email),
        username=Username(user_model.username),
        password=Password(user_model.password),
        role=Role(user_model.role)
    )
    return ShoppinCartAggregate(id=ID_SHO(shoppin_cart_model.id), shoppin_cart=shoppin_cart, product=product, user=user)
