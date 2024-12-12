from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.products.infrastructure.repository.productModel import Product
from app.products.domain.ports.IProductRepository import IProductRepository

class ProductRepository(IProductRepository[Product]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product: Product) -> None:
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)

    async def update_product(self, product: Product) -> Product:
        await self.session.merge(product)
        await self.session.commit()
        return product

    async def delete_product(self, product_id: str) -> Product:
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if product:
            await self.session.delete(product)
            await self.session.commit()
        return product

    async def get_product_by_id(self, product_id: str) -> Product:
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def get_products(self) -> List[Product]:
        result = await self.session.execute(select(Product))
        return result.scalars().all()