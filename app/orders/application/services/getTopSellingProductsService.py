from typing import List, Tuple
from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate

class GetTopSellingProductsService:
    def __init__(self, repo: IOrderRepository[OrderAggregate]):
        self.repo = repo

    async def get_top_selling_products(self, limit: int) -> List[Tuple[str, int]]:
        return await self.repo.get_top_selling_products(limit)