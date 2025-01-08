from app.shopping_cart.domain.ports.IShoppinCartRepository import IShoppinCartRepository
from app.shopping_cart.application.dtos.updateShoppingCartDto import UpdateInventoryDto
from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate

class updateShoppinCartProductService:
    def __init__(self, repo: IShoppinCartRepository[ShoppinCartAggregate]):
        self.repo = repo

    async def update_shoppin_cart_product(self, inventory_aggregate: InventoryAggregate, user_id: str, product_id: str,shoppin_cart_dto: UpdateInventoryDto) -> bool:
        shoppin_cart_aggregate = await self.repo.get_shoppin_cart_product_by_id(inventory_aggregate.inventory.id.get(), user_id, product_id)
        if not shoppin_cart_aggregate:
            raise ValueError(f"No product associated with that id {product_id} in the shopping cart")
        elif shoppin_cart_dto.quantity > inventory_aggregate.inventory.quantity.get():
            raise ValueError(f"Quantity must be less than or equal to the available quantity. Available quantity: " + str(inventory_aggregate.inventory.quantity.get()))
        
        shoppin_cart_aggregate.update(
            quantity=shoppin_cart_dto.quantity
        )

        await self.repo.update_shoppin_cart_product(shoppin_cart_aggregate, inventory_aggregate.inventory.id.get())
        return True