from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate

class GetSalesByProductIdService:
    def __init__(self, repo: IOrderRepository[OrderAggregate]):
        self.repo = repo

    async def get_sales_by_product_id(self, product_id: str) -> int:
        return await self.repo.get_sales_by_product_id(product_id)