from app.shopping_cart.domain.ports.IShoppinCartRepository import IShoppinCartRepository
from app.shopping_cart.application.dtos.addShoppingCartDto import AddShoppiCartDto
from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate
from app.products.domain.aggregate_root import ProductAggregate
from app.users.domain.aggregate.aggregate_user import AggregateUser
from uuid import uuid4

class AddShoppinCartProductService:
    def __init__(self, repo: IShoppinCartRepository[ShoppinCartAggregate]):
        self.repo = repo

    async def add_shoppin_cart_product(self, shoppin_cart_dto: AddShoppiCartDto, product_aggregate: ProductAggregate, user_aggregate: AggregateUser, inventory_id: str) -> ShoppinCartAggregate:
        #Verificacion de si existe un carrito previo 
        existing_shoppin_carts = await self.repo.get_shoppin_cart_products(user_aggregate.user.id.get())
        shoppin_cart: str = ""
        if existing_shoppin_carts:
            for shoppin_cart in existing_shoppin_carts:
                shoppin_cart_id = shoppin_cart.shoppin_cart.id.get()
                break
        else:
            shoppin_cart_id = str(uuid4())
            
        shoppin_cart_aggregate = ShoppinCartAggregate.create(
            id=shoppin_cart_id,
            quantity=shoppin_cart_dto.quantity,
            product_id=shoppin_cart_dto.product_id,
            name=product_aggregate.product.name.get(),
            code=product_aggregate.product.code.get(),
            description=product_aggregate.product.description.get(),
            margin_profit=product_aggregate.product.margin_profit.get(),
            cost=product_aggregate.product.cost.get(),
            status=product_aggregate.product.status.value,
            user_id=user_aggregate.user.id.get(),
            user_name=user_aggregate.user.name.get(),
            username=user_aggregate.user.username.get(),
            email=user_aggregate.user.email.get(),
            password=user_aggregate.user.password.get(),
            role=user_aggregate.user.role.value
        )

        await self.repo.add_shoppin_cart_product(shoppin_cart_aggregate, inventory_id)
        return shoppin_cart_aggregate