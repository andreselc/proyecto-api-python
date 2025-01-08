import pytest
from unittest.mock import AsyncMock, MagicMock
from app.orders.application.services.getOrderById import GetOrderByIdService
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.orders.application.services.createOrder import CreateOrderService
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.shopping_cart.application.services.getShoppinCartProducts import GetShoppinCartProducts
from app.shopping_cart.application.services.deleteShoppinCartProduct import DeleteShoppinCartProductService
from app.inventory.application.services.getInventoryByProductId import GetInventoryByProductIdService
from app.orders.application.services.getOrders import GetOrdersService
from app.orders.domain.aggregate.aggregate_order import OrderAggregate

from app.orders.application.services.cancelOrder import CancelOrderService
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.inventory.application.services.getInventoryById import GetInventoryByIdService
from app.inventory.application.services.updateInventory import UpdateInventoryService
from fastapi import HTTPException
from app.orders.application.dtos.UpdateOrderDTO import UpdateOrderDTO
from app.orders.application.events.orderEventHandler import OrderUpdatedEventHandler
from app.orders.application.services.updateOrderStateById import UpdateOrderStateByIdService

from fastapi import HTTPException

@pytest.fixture
def order_repo():
    return AsyncMock(spec=IOrderRepository)

@pytest.fixture
def inventory_service():
    return AsyncMock(spec=GetInventoryByProductIdService)

@pytest.fixture
def inventory_update_service():
    return AsyncMock(spec=UpdateInventoryService)

@pytest.fixture
def shopping_cart_service():
    return AsyncMock(spec=GetShoppinCartProducts)

@pytest.fixture
def delete_shopping_cart_service():
    return AsyncMock(spec=DeleteShoppinCartProductService)

@pytest.fixture
def create_order_service(order_repo, shopping_cart_service, inventory_service, delete_shopping_cart_service):
    return CreateOrderService(order_repo, shopping_cart_service, inventory_service, delete_shopping_cart_service)

@pytest.fixture
def get_order_by_id_service(order_repo):
    return GetOrderByIdService(order_repo)

@pytest.fixture
def get_orders_service(order_repo):
    return GetOrdersService(order_repo)

@pytest.fixture
def event_handler():
    return MagicMock(spec=OrderUpdatedEventHandler)

@pytest.fixture
def cancel_order_service(order_repo, event_handler, inventory_service, inventory_update_service):
    return CancelOrderService(order_repo, event_handler, inventory_service, inventory_update_service)

@pytest.fixture
def update_order_state_by_id_service(order_repo, inventory_service, inventory_update_service, event_handler):
    return UpdateOrderStateByIdService(order_repo, inventory_service, inventory_update_service, event_handler)


@pytest.mark.asyncio
async def test_create_order_no_cart_products(create_order_service, shopping_cart_service):
    # Configurar el mock del servicio de carrito de compras para devolver una lista vacía
    shopping_cart_service.get_shoppin_cart_products.return_value = []

    # Crear el usuario agregado
    user_aggregate = MagicMock(spec=AggregateUser)
    user_aggregate.user = MagicMock()
    user_aggregate.user.id.get.return_value = "user123"
    user_aggregate.user.name.get.return_value = "John Doe"
    user_aggregate.user.username.get.return_value = "johndoe"
    user_aggregate.user.email.get.return_value = "john.doe@example.com"
    user_aggregate.user.password.get.return_value = "password"
    user_aggregate.user.role.value = "customer"

    # Verificar que se lanza una excepción cuando no hay productos en el carrito
    with pytest.raises(HTTPException, match="No shopping cart found for user with id user123"):
        await create_order_service.create_order("user123", user_aggregate)


@pytest.mark.asyncio
async def test_get_order_by_id_success(get_order_by_id_service, order_repo):
    # Configurar el mock del repositorio para devolver una orden
    order_aggregate = MagicMock(spec=OrderAggregate)
    order_repo.get_order_by_id.return_value = order_aggregate

    # Llamar al método get_order_by_id
    result = await get_order_by_id_service.get_order_by_id("order123")

    # Verificar que la orden fue obtenida
    order_repo.get_order_by_id.assert_called_once_with("order123")
    assert result == order_aggregate

@pytest.mark.asyncio
async def test_get_order_by_id_not_found(get_order_by_id_service, order_repo):
    # Configurar el mock del repositorio para devolver None
    order_repo.get_order_by_id.return_value = None

    # Verificar que se lanza una excepción cuando la orden no se encuentra
    with pytest.raises(ValueError, match="Order with id order123 not found"):
        await get_order_by_id_service.get_order_by_id("order123")

@pytest.mark.asyncio
async def test_list_orders_success(get_orders_service, order_repo):
    # Configurar el mock del repositorio para devolver órdenes
    order_aggregate = MagicMock(spec=OrderAggregate)
    order_repo.get_orders.return_value = [order_aggregate]

    # Llamar al método list_orders
    result = await get_orders_service.list_orders("user123")

    # Verificar que las órdenes fueron obtenidas
    order_repo.get_orders.assert_called_once_with("user123")
    assert result == [order_aggregate]

@pytest.mark.asyncio
async def test_list_orders_not_found(get_orders_service, order_repo):
    # Configurar el mock del repositorio para devolver una lista vacía
    order_repo.get_orders.return_value = []

    # Verificar que se lanza una excepción cuando no se encuentran órdenes
    with pytest.raises(ValueError, match="No orders found for user with id user123"):
        await get_orders_service.list_orders("user123")

@pytest.mark.asyncio
async def test_cancel_order_not_found(cancel_order_service, order_repo):
    # Configurar el mock del repositorio para devolver None
    order_repo.get_order_by_id.return_value = None

    # Crear el DTO de actualización de la orden
    order_dto = UpdateOrderDTO(status="cancelled")

    # Verificar que se lanza una excepción cuando la orden no se encuentra
    with pytest.raises(ValueError, match="Order with id order123 not found"):
        await cancel_order_service.cancel_order("order123", "user123", "customer", order_dto)

@pytest.mark.asyncio
async def test_cancel_order_no_permission(cancel_order_service, order_repo):
    # Configurar el mock del repositorio para devolver una orden
    order_aggregate = MagicMock(spec=OrderAggregate)
    order_aggregate.user = MagicMock()
    order_aggregate.user.id.get.return_value = "other_user"
    order_repo.get_order_by_id.return_value = order_aggregate

    # Crear el DTO de actualización de la orden
    order_dto = UpdateOrderDTO(status="cancelled")

    # Verificar que se lanza una excepción cuando el usuario no tiene permiso para cancelar la orden
    with pytest.raises(HTTPException, match="You do not have permission to cancel this order"):
        await cancel_order_service.cancel_order("order123", "user123", "customer", order_dto)

@pytest.mark.asyncio
async def test_cancel_order_not_pending(cancel_order_service, order_repo):
    # Configurar el mock del repositorio para devolver una orden
    order_aggregate = MagicMock(spec=OrderAggregate)
    order_aggregate.user = MagicMock()
    order_aggregate.user.id.get.return_value = "user123"
    order_aggregate.order = MagicMock()
    order_aggregate.order.status.value = "completed"
    order_repo.get_order_by_id.return_value = order_aggregate

    # Crear el DTO de actualización de la orden
    order_dto = UpdateOrderDTO(status="cancelled")

    # Verificar que se lanza una excepción cuando la orden no está pendiente
    with pytest.raises(HTTPException, match="Customers can only cancel pending orders"):
        await cancel_order_service.cancel_order("order123", "user123", "customer", order_dto)


@pytest.mark.asyncio
async def test_update_order_state_by_id_not_found(update_order_state_by_id_service, order_repo):
    # Configurar el mock del repositorio para devolver None
    order_repo.get_order_by_id.return_value = None

    # Crear el DTO de actualización de la orden
    order_dto = UpdateOrderDTO(status="completed")

    # Verificar que se lanza una excepción cuando la orden no se encuentra
    with pytest.raises(ValueError, match="Order with id order123 not found"):
        await update_order_state_by_id_service.update_order_state_by_id("order123", "manager", order_dto)

@pytest.mark.asyncio
async def test_update_order_state_by_id_no_permission(update_order_state_by_id_service, order_repo):
    # Configurar el mock del repositorio para devolver una orden
    order_aggregate = MagicMock(spec=OrderAggregate)
    order_repo.get_order_by_id.return_value = order_aggregate

    # Crear el DTO de actualización de la orden
    order_dto = UpdateOrderDTO(status="completed")

    # Verificar que se lanza una excepción cuando el usuario no tiene permiso para actualizar la orden
    with pytest.raises(PermissionError, match="Only managers can update the order status to completed"):
        await update_order_state_by_id_service.update_order_state_by_id("order123", "customer", order_dto)