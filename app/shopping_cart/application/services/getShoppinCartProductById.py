from app.shopping_cart.domain.ports.IShoppinCartRepository import IShoppinCartRepository
from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate

class GetShoppinCartProductById:
    def __init__(self, repo: IShoppinCartRepository[ShoppinCartAggregate]):
        self.repo = repo

    async def get_shoppin_cart_product_by_id(self, product_id: str) -> ShoppinCartAggregate:
        shoppin_cart_aggregate = await self.repo.get_shoppin_cart_product_by_id(product_id)
        if not shoppin_cart_aggregate:
            raise ValueError(f"Product with id {product_id} not added to shopping cart")
        return shoppin_cart_aggregate