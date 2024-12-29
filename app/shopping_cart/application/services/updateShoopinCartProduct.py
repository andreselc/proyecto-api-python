from app.shopping_cart.domain.ports.IShoppinCartRepository import IShoppinCartRepository
from app.shopping_cart.application.dtos.updateShoppingCartDto import UpdateInventoryDto
from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate

class updateShoppinCartProductService:
    def __init__(self, repo: IShoppinCartRepository[ShoppinCartAggregate]):
        self.repo = repo

    async def update_shoppin_cart_product(self, shoppin_cart_id: str, shoppin_cart_dto: UpdateInventoryDto) -> bool:
        shoppin_cart_aggregate = await self.repo.get_shoppin_cart_product_by_id(shoppin_cart_id)
        if not shoppin_cart_aggregate:
            raise ValueError(f"No product associated with that id {shoppin_cart_id}")
        
        shoppin_cart_aggregate.update(
            quantity=shoppin_cart_dto.quantity
        )

        await self.repo.update_shoppin_cart_product(shoppin_cart_aggregate)
        return True