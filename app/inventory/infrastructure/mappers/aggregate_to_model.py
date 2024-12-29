from app.common.infrastructure.Modelo import InventoryModel
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate
from datetime import datetime, timezone

def aggregate_to_model(inventory_aggregate: InventoryAggregate) -> InventoryModel:
    return InventoryModel(
        id=inventory_aggregate.inventory.id.get(),
        quantity=inventory_aggregate.inventory.quantity.get(),
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        product_id=inventory_aggregate.product.id.get()
    )