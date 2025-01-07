from app.inventory.domain.ports.IInventoryRepository import IInventoryRepository
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate

class GetInventoryByProductIdService:
    def __init__(self, repo: IInventoryRepository[InventoryAggregate]):
        self.repo = repo

    async def get_inventory_by_product_id(self, product_id: str) -> InventoryAggregate:
        inventory_aggregate = await self.repo.get_inventory_by_product_id(product_id)
        if not inventory_aggregate:
            raise ValueError(f"There is no product with that id {product_id} associated with an inventory ")
        return inventory_aggregate