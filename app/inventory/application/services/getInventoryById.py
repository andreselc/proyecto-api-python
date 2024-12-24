from app.inventory.domain.ports.IInventoryRepository import IInventoryRepository
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate

class GetInventoryByIdService:
    def __init__(self, repo: IInventoryRepository[InventoryAggregate]):
        self.repo = repo

    async def get_inventory_by_id(self, inventory_id: str) -> InventoryAggregate:
        inventory_aggregate = await self.repo.get_inventory_by_id(inventory_id)
        if not inventory_aggregate:
            raise ValueError(f"Inventory with id {inventory_id} not found")
        return inventory_aggregate