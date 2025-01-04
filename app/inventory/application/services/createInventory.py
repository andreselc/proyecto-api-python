from app.inventory.domain.ports.IInventoryRepository import IInventoryRepository
from app.inventory.application.dtos.createInventoryDto import CreateInventoryDto
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate
from app.products.domain.aggregate_root import ProductAggregate

class CreateInventoryService:
    def __init__(self, repo: IInventoryRepository[InventoryAggregate]):
        self.repo = repo

    async def create_inventory(self, inventory_dto: CreateInventoryDto, product_aggregate: ProductAggregate) -> InventoryAggregate:
        
        inventory_aggregate = InventoryAggregate.create(
            quantity=inventory_dto.quantity,
            product_id=inventory_dto.product_id,
            name=product_aggregate.product.name.get(),
            code=product_aggregate.product.code.get(),
            description=product_aggregate.product.description.get(),
            margin_profit=product_aggregate.product.margin_profit.get(),
            cost=product_aggregate.product.cost.get(),
            status="active"
        )
        await self.repo.create_inventory(inventory_aggregate)
        return inventory_aggregate
