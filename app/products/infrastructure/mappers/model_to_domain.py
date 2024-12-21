from app.products.infrastructure.repository.productModel import ProductModel
from app.products.domain.aggregate_root import ProductAggregate
from app.products.domain.entities.product import Product
from app.products.domain.value_objects.id import ID
from app.products.domain.value_objects.name import Name
from app.products.domain.value_objects.description import Description
from app.products.domain.value_objects.code import Code
from app.products.domain.value_objects.price import Price
from app.products.domain.value_objects.margin_profit import MarginProfit
from app.products.domain.value_objects.cost import Cost
from app.products.domain.enums.status import Status

def model_to_domain(product_model: ProductModel) -> ProductAggregate:
    product = Product(
        id=ID(product_model.id),
        name=Name(product_model.name),
        code=Code(product_model.code),
        description=Description(product_model.description),
        price=Price(product_model.price),
        margin_profit=MarginProfit(product_model.profit_margin),
        cost=Cost(product_model.cost),
        status=Status(product_model.status)
    )
    return ProductAggregate(id=ID(product_model.id), product=product)