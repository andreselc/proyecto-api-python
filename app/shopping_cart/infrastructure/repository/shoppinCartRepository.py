from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.common.infrastructure.Modelo import ShoppinCartModel, User, ProductModel, InventoryModel
from app.shopping_cart.domain.ports.IShoppinCartRepository import IShoppinCartRepository
from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate
from app.shopping_cart.infrastructure.mappers.aggregate_to_model import aggregate_to_model
from app.shopping_cart.infrastructure.mappers.model_to_domain import model_to_domain

class ShoppingCartRepository(IShoppinCartRepository[ShoppinCartAggregate]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_shoppin_cart_product(self, shoppin_cart_aggregate: ShoppinCartAggregate, inventory_id: str) -> None:
        shoppin_cart_model = aggregate_to_model(shoppin_cart_aggregate, inventory_id)
        self.session.add(shoppin_cart_model)
        await self.session.commit()
        await self.session.refresh(shoppin_cart_model)

    async def update_shoppin_cart_product(self, shoppin_cart_aggregate: ShoppinCartAggregate, inventory_id: str) -> ShoppinCartAggregate:
        shoppin_cart_model =aggregate_to_model(shoppin_cart_aggregate, inventory_id)
        await self.session.merge(shoppin_cart_model)
        await self.session.commit()
        return shoppin_cart_model
    
    async def delete_shoppin_cart_product(self, inventory_id: str, user_id: str):
        result = await self.session.execute(
            select(ShoppinCartModel).where((ShoppinCartModel.inventory_id == inventory_id) & (ShoppinCartModel.user_id == user_id))
            )
        shoppin_cart_model = result.scalar_one_or_none()
        if shoppin_cart_model:
            await self.session.delete(shoppin_cart_model)
            await self.session.commit()

    async def get_shoppin_cart_product_by_id(self, inventory_id: str, user_id: str, product_id: str):
        result = await self.session.execute(
            select(ShoppinCartModel).where((ShoppinCartModel.inventory_id == inventory_id) & (ShoppinCartModel.user_id == user_id))
            )
        shoppin_cart_model = result.scalar_one_or_none()
        if shoppin_cart_model:
            result2 = await self.session.execute(select(ProductModel).where(ProductModel.id == product_id))
            product_model = result2.scalar_one_or_none()
            result3 = await self.session.execute(select(User).where(User.id == user_id))
            user_model = result3.scalar_one_or_none()
            return model_to_domain(shoppin_cart_model, product_model, user_model)
        return None
    
    async def get_shoppin_cart_products(self, user_id: str) -> List[ShoppinCartAggregate]:
        products_list = []
        result = await self.session.execute(select(ShoppinCartModel).where(ShoppinCartModel.user_id == user_id))
        shoppin_carts_models = result.scalars().all()
        for shoppin_cart_model in shoppin_carts_models:
            result2 = await self.session.execute(select(InventoryModel).where(InventoryModel.id == shoppin_cart_model.inventory_id))
            inventory_model = result2.scalar_one_or_none()
            result3 = await self.session.execute(select(ProductModel).where(ProductModel.id == inventory_model.product_id))
            product_model = result3.scalar_one_or_none()
            result4 = await self.session.execute(select(User).where(User.id == user_id))
            user_model = result4.scalar_one_or_none()
            products_list.append(model_to_domain(shoppin_cart_model, product_model, user_model))
        return [product for product in products_list]
        