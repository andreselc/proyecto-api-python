from app.shopping_cart.domain.ports.IShoppinCartRepository import IShoppinCartRepository
from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate

class DeleteShoppinCartProductService:
    def __init__(self, repo: IShoppinCartRepository[ShoppinCartAggregate]):
        self.repo = repo

    async def delete_shoppin_cart_product(self, inventory_id: str, user_id: str, product_id: str) -> bool:
        Shoppin_cart_aggregate = await self.repo.get_shoppin_cart_product_by_id(inventory_id, user_id, product_id)
        if not Shoppin_cart_aggregate:
            raise ValueError(f"Product with inventory id {inventory_id} not added")
        await self.repo.delete_shoppin_cart_product(inventory_id, user_id)
        return True