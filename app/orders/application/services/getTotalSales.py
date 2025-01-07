from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate

class GetTotalSalesService:
    def __init__(self, repo: IOrderRepository[OrderAggregate]):
        self.repo = repo

    async def get_total_sales(self) -> int:
        return await self.repo.get_total_sales()