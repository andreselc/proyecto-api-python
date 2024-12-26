from app.inventory.domain.ports.IInventoryRepository import IInventoryRepository
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate
from sqlalchemy.ext.asyncio import AsyncSession
from app.inventory.infrastructure.model.inventoryModel import InventoryModel
from sqlalchemy.future import select
from app.inventory.infrastructure.mappers.aggregate_to_model import aggregate_to_model
from app.inventory.infrastructure.mappers.model_to_domain import model_to_domain
from datetime import datetime

class InventoryRepository(InventoryAggregate[InventoryAggregate]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, inventory_aggregate: InventoryAggregate) -> None:
        inventory_model = aggregate_to_model(inventory_aggregate)
        self.session.add(inventory_model)
        await self.session.commit()
        await self.session.refresh(inventory_model)

