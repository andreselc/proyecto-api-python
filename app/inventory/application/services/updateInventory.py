from app.inventory.application.dtos.updateInventoryDto import UpdateInventoryDto
from app.inventory.domain.ports.IInventoryRepository import IInventoryRepository
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate

class UpdateInventoryService:
    def __init__(self, repo: IInventoryRepository[InventoryAggregate]):
        self.repo = repo

    async def update_inventory(self, inventory_id: str, inventory_dto: UpdateInventoryDto) -> bool:
        inventory_aggregate = await self.repo.get_inventory_by_id(inventory_id)
        if not inventory_aggregate:
            raise ValueError(f"Inventory with id {inventory_id} not found")
        
        inventory_aggregate.update(
            quantity=inventory_dto.quantity,
            name=inventory_aggregate.product.name.get(),
            code=inventory_aggregate.product.code.get(),
            description=inventory_aggregate.product.description.get(),
            margin_profit=inventory_aggregate.product.margin_profit.get(),
            cost=inventory_aggregate.product.cost.get(),
            status=inventory_aggregate.product.status.value
        )

        await self.repo.update_inventory(inventory_aggregate)
        return True