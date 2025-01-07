from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate

class GetOrdersService:
    def __init__(self, repo: IOrderRepository[OrderAggregate]):
        self.repo = repo

    async def list_orders(self, user_id: str) -> list[OrderAggregate]:
        orders = await self.repo.get_orders(user_id)
        if not orders:
            raise ValueError(f"No orders found for user with id {user_id}")
        return orders