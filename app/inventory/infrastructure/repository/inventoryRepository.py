from app.inventory.domain.ports.IInventoryRepository import IInventoryRepository
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate
from sqlalchemy.ext.asyncio import AsyncSession
from app.inventory.infrastructure.model.inventoryModel import InventoryModel
from app.products.infrastructure.repository.productModel import ProductModel
from sqlalchemy.future import select
from app.inventory.infrastructure.mappers.aggregate_to_model import aggregate_to_model
from app.inventory.infrastructure.mappers.model_to_domain import model_to_domain
from datetime import datetime

class InventoryRepository(IInventoryRepository[InventoryAggregate]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_inventory(self, inventory_aggregate: InventoryAggregate, product_id: str, ) -> None:
        inventory_model = aggregate_to_model(inventory_aggregate, product_id)
        self.session.add(inventory_model)
        await self.session.commit()
        await self.session.refresh(inventory_model)

    async def update_inventory(self, inventory_aggregate: InventoryAggregate) -> InventoryAggregate:
        inventory_model = aggregate_to_model(inventory_aggregate)
        inventory_model.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await self.session.merge(inventory_model)
        await self.session.commit()

    async def get_inventory_by_id(self, inventory_id: str) -> InventoryAggregate:
        result = await self.session.execute(select(InventoryModel).where(InventoryModel.id == inventory_id))
        inventory_model = result.scalar_one_or_none()
        if inventory_model: 
            result2 = await self.session.execute(select(ProductModel).where(ProductModel.id == inventory_model.product_id))
            product_model = result2.scalar_one_or_none()
            return model_to_domain(inventory_model, product_model)
        return None




