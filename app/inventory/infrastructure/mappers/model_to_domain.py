from app.common.infrastructure.Modelo import InventoryModel, ProductModel
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate
from app.inventory.domain.entities.inventory import Inventory
from app.inventory.domain.value_objects.id import ID as ID_INV
from app.inventory.domain.value_objects.quantity import Quantity
from app.products.domain.value_objects.id import ID as ID_PRO
from app.products.domain.value_objects.name import Name
from app.products.domain.value_objects.description import Description
from app.products.domain.value_objects.code import Code
from app.products.domain.value_objects.price import Price
from app.products.domain.value_objects.margin_profit import MarginProfit
from app.products.domain.value_objects.cost import Cost
from app.products.domain.enums.status import Status
from app.products.domain.entities.product import Product
from app.inventory.domain.entities.inventory import Inventory

def model_to_domain(inventory_model: InventoryModel, product_model: ProductModel) -> InventoryAggregate:
    inventory = Inventory(
        id = ID_INV(inventory_model.id),
        quantity = Quantity(inventory_model.quantity)
    )
    product = Product(
        id=ID_PRO(product_model.id),
        name=Name(product_model.name),
        code=Code(product_model.code),
        description=Description(product_model.description),
        price=Price(product_model.price),
        margin_profit=MarginProfit(product_model.profit_margin),
        cost=Cost(product_model.cost),
        status=Status(product_model.status)
    )
    return InventoryAggregate(id=ID_INV(inventory_model.id), inventory=inventory, product=product)