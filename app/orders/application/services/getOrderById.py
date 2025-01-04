from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate

class GetOrderById:
    def __init__(self, repo: IOrderRepository[OrderAggregate]):
        self.repo = repo

    async def get_order_by_id(self, order_id: str) -> OrderAggregate:
        order_aggregate = await self.repo.get_order_by_id(order_id)
        if not order_aggregate:
            raise ValueError(f"Order with id {order_id} not found")
        return order_aggregate