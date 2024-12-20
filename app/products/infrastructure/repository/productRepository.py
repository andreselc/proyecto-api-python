from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.products.infrastructure.repository.productModel import ProductModel
from app.products.domain.ports.IProductRepository import IProductRepository
from app.products.domain.aggregate_root import ProductAggregate
from app.products.infrastructure.mappers.aggregate_to_model import aggregate_to_model
from datetime import datetime

class ProductRepository(IProductRepository[ProductAggregate]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product_aggregate: ProductAggregate) -> None:
        product_model = aggregate_to_model(product_aggregate)
        self.session.add(product_model)
        await self.session.commit()
        await self.session.refresh(product_model)

    async def update_product(self, product_aggregate: ProductAggregate) -> ProductAggregate:
        product_model = aggregate_to_model(product_aggregate)
        product_model.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Establecer el valor de updated_at como cadena de texto
        await self.session.merge(product_model)
        await self.session.commit()
        return product_aggregate

    async def delete_product(self, product_id: str) -> ProductAggregate:
        result = await self.session.execute(select(ProductModel).where(ProductModel.id == product_id))
        product_model = result.scalar_one_or_none()
        if product_model:
            await self.session.delete(product_model)
            await self.session.commit()
        return ProductAggregate(product_model)

    async def get_product_by_id(self, product_id: str) -> ProductAggregate:
        result = await self.session.execute(select(ProductModel).where(ProductModel.id == product_id))
        product_model = result.scalar_one_or_none()
        if product_model:
            return ProductAggregate(product_model)
        return None

    async def get_products(self) -> List[ProductAggregate]:
        result = await self.session.execute(select(ProductModel))
        product_models = result.scalars().all()
        return [ProductAggregate(product_model) for product_model in product_models]