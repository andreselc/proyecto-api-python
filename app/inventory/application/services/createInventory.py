from app.inventory.domain.ports.IInventoryRepository import IInventoryRepository
from app.inventory.application.dtos.createInventoryDto import CreateInventoryDto
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate
from app.products.domain.aggregate_root import ProductAggregate

class CreateInventoryService:
    def __init__(self, repo: IInventoryRepository[InventoryAggregate]):
        self.repo = repo

    async def create_inventory(self, inventory_dto: CreateInventoryDto) -> InventoryAggregate:
        #verificar si ya el producto por su codigo ya se encuentra asociado a un inventario
        #esta pendiente!
        inventory_aggregate = InventoryAggregate.create(
            quantity=inventory_dto.quantity,
            name=inventory_dto.name,
            code=inventory_dto.code,
            description=inventory_dto.description,
            margin_profit=inventory_dto.profit_margin,
            cost=inventory_dto.cost,
            status="active"
        )
        await self.repo.create_inventory(inventory_aggregate, inventory_dto.product_id)
        return inventory_aggregate
