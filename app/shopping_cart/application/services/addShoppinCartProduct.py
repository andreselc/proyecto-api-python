from app.shopping_cart.domain.ports.IShoppinCartRepository import IShoppinCartRepository
from app.shopping_cart.application.dtos.addShoppingCartDto import AddShoppiCartDto
from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate
from app.products.domain.aggregate_root import ProductAggregate
from app.users.domain.aggregate.aggregate_user import AggregateUser

class AddShoppinCartProductService:
    def __init__(self, repo: IShoppinCartRepository[ShoppinCartAggregate]):
        self.repo = repo

    async def add_shoppin_cart_product(self, shoppin_cart_dto: AddShoppiCartDto, product_aggregate: ProductAggregate, user_aggregate: AggregateUser) -> ShoppinCartAggregate:

        shoppin_cart_aggregate = ShoppinCartAggregate.create(
            quantity=shoppin_cart_dto.quantity,
            product_id=shoppin_cart_dto.product_id,
            name=product_aggregate.product.name.get(),
            code=product_aggregate.product.code.get(),
            description=product_aggregate.product.description.get(),
            margin_profit=product_aggregate.product.margin_profit.get(),
            cost=product_aggregate.product.cost.get(),
            status=product_aggregate.product.status.value,
            user_name=user_aggregate.user.name.get(),
            username=user_aggregate.user.username.get(),
            email=user_aggregate.user.email.get(),
            password=user_aggregate.user.password.get(),
            role=user_aggregate.user.role.value
        )

        await self.repo.add_shoppin_cart_product(shoppin_cart_aggregate)
        return shoppin_cart_aggregate