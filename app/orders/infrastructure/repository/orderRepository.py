from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.common.infrastructure.Modelo import OrderModel, ProductModel, User, InventoryModel, OrderItem
from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate
from app.orders.infrastructure.mappers.model_to_domain import model_to_domain
from app.orders.infrastructure.mappers.aggregate_to_model import aggregate_to_model
from app.orders.infrastructure.mappers.aggregate_to_model_OrderItem import aggregate_to_model_order_item
from app.common.infrastructure.Modelo import OrderItem
from datetime import datetime

class OrderRepository(IOrderRepository[OrderAggregate]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, order_aggregate: OrderAggregate) -> None:
        order_model = aggregate_to_model(order_aggregate)
        self.session.add(order_model)
        await self.session.commit()
        await self.session.refresh(order_model)

    async def update_order_state_by_id(self, order_aggregate: OrderAggregate) -> OrderAggregate:
        order_model = await self.session.get(OrderModel, order_aggregate.id.get())
        if order_model:
            order_model.status = "completed"
            order_model.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await self.session.merge(order_model)
            await self.session.commit()
            order_aggregate.update(status="completed")
        return order_aggregate
    
    async def get_order_by_id(self, order_id: str) -> OrderAggregate:
        result = await self.session.execute(select(OrderModel).where(OrderModel.id == order_id))
        order_model = result.scalar_one_or_none()
        if order_model:
            order_items_result = await self.session.execute(select(OrderItem).where(OrderItem.order_id == order_id))
            order_items = order_items_result.scalars().all()
            product_models = []
            for order_item in order_items:
                inventory_result = await self.session.execute(select(InventoryModel).where(InventoryModel.id == order_item.inventory_id))
                inventory_model = inventory_result.scalar_one_or_none()
                if inventory_model:
                    product_result = await self.session.execute(select(ProductModel).where(ProductModel.id == inventory_model.product_id))
                    product_model = product_result.scalar_one_or_none()
                    if product_model:
                        product_models.append(product_model)
            user_result = await self.session.execute(select(User).where(User.id == order_model.user_id))
            user_model = user_result.scalar_one_or_none()
            return model_to_domain(order_model, product_models, user_model)
        return None

    async def get_orders(self, user_id: str) -> List[OrderAggregate]:
        result = await self.session.execute(select(OrderModel).where(OrderModel.user_id == user_id))
        order_models = result.scalars().all()
        orders = []
        for order_model in order_models:
            order_items_result = await self.session.execute(select(OrderItem).where(OrderItem.order_id == order_model.id))
            order_items = order_items_result.scalars().all()
            product_models = []
            for order_item in order_items:
                inventory_result = await self.session.execute(select(InventoryModel).where(InventoryModel.id == order_item.inventory_id))
                inventory_model = inventory_result.scalar_one_or_none()
                if inventory_model:
                    product_result = await self.session.execute(select(ProductModel).where(ProductModel.id == inventory_model.product_id))
                    product_model = product_result.scalar_one_or_none()
                    if product_model:
                        product_models.append(product_model)
            user_result = await self.session.execute(select(User).where(User.id == order_model.user_id))
            user_model = user_result.scalar_one_or_none()
            orders.append(model_to_domain(order_model, product_models, user_model))
        return orders

    async def cancel_order(self, order_aggregate: OrderAggregate) -> OrderAggregate:
        order_model = await self.session.get(OrderModel, order_aggregate.id.get())
        if order_model:
            order_model.status = "canceled"
            order_model.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("Entre aqui 4")
            await self.session.merge(order_model)
            await self.session.commit()
        return order_aggregate
    

    async def create_order_item(self, order_item: OrderItem) -> None:
        self.session.add(order_item)
        await self.session.commit()
        await self.session.refresh(order_item)

    async def get_order_items(self, order_id: str) -> List[Tuple[str, int]]:
        result = await self.session.execute(select(OrderItem).where(OrderItem.order_id == order_id))
        order_items = result.scalars().all()
        return [(order_item.inventory_id, order_item.quantity) for order_item in order_items]
    

    
    
    