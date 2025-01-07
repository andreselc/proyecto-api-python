from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.shopping_cart.application.services.getShoppinCartProducts import GetShoppinCartProducts
from app.shopping_cart.application.services.deleteShoppinCartProduct import DeleteShoppinCartProductService
from uuid import uuid4
from app.orders.infrastructure.mappers.aggregate_to_model_OrderItem import aggregate_to_model_order_item
from app.inventory.application.services.getInventoryByProductId import GetInventoryByProductIdService
from fastapi import HTTPException, status

class CreateOrderService:
    def __init__(self, repo: IOrderRepository[OrderAggregate], shopping_cart_service: GetShoppinCartProducts, inventory_service: GetInventoryByProductIdService, delete_shopping_cart_service: DeleteShoppinCartProductService):
        self.repo = repo
        self.shopping_cart_service = shopping_cart_service
        self.inventory_service = inventory_service
        self.delete_shopping_cart_service = delete_shopping_cart_service

    async def create_order(self, user_id: str, user_aggregate: AggregateUser) -> OrderAggregate:
         
        # Obtener los productos del carrito del usuario
        cart_products = await self.shopping_cart_service.get_shoppin_cart_products(user_id)
        
        if not cart_products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No shopping cart found for user with id {user_id}")
        
        # Extraer los productos de los objetos ShoppinCartAggregate
        products = [cart_product.product for cart_product in cart_products]

        # Crear la orden a partir de los productos del carrito
        order_aggregate = OrderAggregate.create(
            id=str(uuid4()),
            status="pending",
            products=products,
            user_id=user_aggregate.user.id.get(),
            user_name=user_aggregate.user.name.get(),
            username=user_aggregate.user.username.get(),
            email=user_aggregate.user.email.get(),
            password=user_aggregate.user.password.get(),
            role=user_aggregate.user.role.value
        )

        # Guardar la orden en la base de datos
        await self.repo.create_order(order_aggregate)

        # Crear los items de la orden en la base de datos
        for product, cart_product in zip(order_aggregate.products, cart_products):
            product_id_str = str(product.id.get())  # Convertir el ID del producto a cadena
            inventory_aggregate = await self.inventory_service.get_inventory_by_product_id(product_id_str)
            order_item = aggregate_to_model_order_item(order_aggregate, inventory_aggregate, cart_product)
            await self.repo.create_order_item(order_item)
            await self.delete_shopping_cart_service.delete_shoppin_cart_product(inventory_aggregate.id.get(), user_id, cart_product.product.id.get())

        return order_aggregate