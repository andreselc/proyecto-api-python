from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate
from app.inventory.application.dtos.inventoryDto import InventoryDto

def domain_to_dto(inventory_aggregate: InventoryAggregate) -> InventoryDto:
    inventory, product = inventory_aggregate.get()
    return InventoryDto(
        id=inventory.id.get(),
        quantity=inventory.quantity.get(),
        productName=product.name.get(),
        productCode=product.code.get(),
        productStatus=product.status.value
    )