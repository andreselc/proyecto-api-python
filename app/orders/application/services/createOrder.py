from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.products.domain.aggregate_root import ProductAggregate
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.shopping_cart.application.services.getShoppinCartProducts import GetShoppinCartProducts
from uuid import uuid4

class CreateOrderService:
    def __init__(self, repo: IOrderRepository[OrderAggregate], shopping_cart_service: GetShoppinCartProducts):
        self.repo = repo
        self.shopping_cart_service = shopping_cart_service

    async def create_order(self, user_id: str, user_aggregate: AggregateUser) -> OrderAggregate:
        # Obtener los productos del carrito del usuario
        cart_products = await self.shopping_cart_service.get_shoppin_cart_products(user_id)

        if not cart_products:
            raise ValueError(f"No shopping cart found for user with id {user_id}")
        
        # Crear la orden a partir de los productos del carrito
        order_aggregate = OrderAggregate.create(
            id=str(uuid4()),
            status="pending",
            products=cart_products,
            user_id=user_aggregate.user.id.get(),
            user_name=user_aggregate.user.name.get(),
            username=user_aggregate.user.username.get(),
            email=user_aggregate.user.email.get(),
            password=user_aggregate.user.password.get(),
            role=user_aggregate.user.role.value
        )

        await self.repo.create_order(order_aggregate)
        return order_aggregate