import uuid
from app.common.infrastructure.Modelo import OrderItem
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate
from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate

def aggregate_to_model_order_item(order_aggregate: OrderAggregate, inventory_aggregate: InventoryAggregate, shopping_cart_aggregate: ShoppinCartAggregate) -> OrderItem:
    return OrderItem(
        id = str(uuid.uuid4()),
        order_id=order_aggregate.id,
        inventory_id=inventory_aggregate.id.get(),
        quantity=shopping_cart_aggregate.shoppin_cart.quantity.get(),
    )