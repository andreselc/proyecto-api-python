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
            name=inventory_dto.name,
            code=inventory_dto.code,
            description=inventory_dto.description,
            margin_profit=inventory_dto.profit_margin,
            cost=inventory_dto.cost,
            status=inventory_dto.status
        )

        await self.repo.update_inventory(inventory_aggregate)
        return True