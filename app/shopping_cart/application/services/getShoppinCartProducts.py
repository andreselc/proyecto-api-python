from app.shopping_cart.domain.ports.IShoppinCartRepository import IShoppinCartRepository
from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate

class GetShoppinCartProducts:
    def __init__(self, repo: IShoppinCartRepository[ShoppinCartAggregate]):
        self.repo = repo

    async def get_shoppin_cart_products(self, user_id: str) -> list[ShoppinCartAggregate]:
        return await self.repo.get_shoppin_cart_products(user_id)