from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional
from app.orders.application.services.createOrder import CreateOrderService
from app.orders.application.services.updateOrderStateById import UpdateOrderStateByIdService
from app.orders.application.services.getOrderById import GetOrderByIdService
from app.orders.application.services.getOrders import GetOrdersService
from app.orders.application.services.cancelOrder import CancelOrderService
from app.shopping_cart.application.services.getShoppinCartProducts import GetShoppinCartProducts
from app.shopping_cart.application.services.deleteShoppinCartProduct import DeleteShoppinCartProductService
from app.inventory.application.services.getInventoryByProductId import GetInventoryByProductIdService
from app.inventory.application.services.getInventoryById import GetInventoryByIdService
from app.inventory.application.services.updateInventory import UpdateInventoryService
from app.users.application.services.GetUserById import GetUserById
#from app.orders.application.dtos import OrderDTO, UpdateOrderDTO
from app.orders.application.dtos.UpdateOrderDTO import UpdateOrderDTO
from app.shopping_cart.application.dtos.updateShoppingCartDto import UpdateInventoryDto
from app.orders.infrastructure.repository.orderRepository import OrderRepository
from app.products.infrastructure.repository.productRepository import ProductRepository
from app.inventory.infrastructure.repository.inventoryRepository import InventoryRepository
from app.shopping_cart.infrastructure.repository.shoppinCartRepository import ShoppingCartRepository
from app.users.infrastructure.repository.UserRepository import UserRepository
from app.orders.infrastructure.db import database
from app.orders.infrastructure.mappers.domain_to_dto import domain_to_dto
from app.users.auth.auth import get_current_user
from app.users.auth.Role_Checker import RoleChecker
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.common.infrastructure.Modelo import User

router = APIRouter(
    tags=["Orders"]
)

@router.post("/orders/create_orders", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleChecker(["customer"]))])
async def create_order(current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(database.get_session)):
    repo = OrderRepository(session)
    repoI = InventoryRepository(session)
    repoS = ShoppingCartRepository(session)
    repoU = UserRepository(session)
    user_service = GetUserById(repoU)
    shopping_cart_service = GetShoppinCartProducts(repoS)
    delete_shopping_cart_service = DeleteShoppinCartProductService(repoS)
    inventory_service = GetInventoryByProductIdService(repoI)
    order_service = CreateOrderService(repo, shopping_cart_service, inventory_service, delete_shopping_cart_service)
    try:
        user_id = current_user.id
        user_aggregate = await user_service.get_user_by_id(user_id, False)
        order_aggregate = await order_service.create_order(user_id, user_aggregate)
        #order_dto = domain_to_dto(order_aggregate)
        return {"message": "Order created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["customer", "manager"]))])
async def get_orders_by_user(current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(database.get_session), user_id: Optional[str] = Query(None)):
    repo = OrderRepository(session)
    order_service = GetOrdersService(repo)
    try:
        if current_user.role == "customer" or (current_user.role == "manager" and not user_id):
            user_id = current_user.id
        order_aggregates = await order_service.list_orders(user_id)
        orders = [domain_to_dto(order) for order in order_aggregates]
        return orders
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/orders/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["manager"]))])
async def get_order_by_id(order_id: str, session: AsyncSession = Depends(database.get_session)):
    repo = OrderRepository(session)
    order_service = GetOrderByIdService(repo)
    try:
        order_aggregate = await order_service.get_order_by_id(order_id)
        return domain_to_dto(order_aggregate)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# @router.patch("/orders/update/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["manager"]))], response_model=None)
# async def update_order_as_completed(current_user: Annotated[User, Depends(get_current_user)], order_id: str, order_dto: UpdateOrderDTO, session: AsyncSession = Depends(database.get_session)):
#     repo = OrderRepository(session)
#     order_service = UpdateOrderStateByIdService(repo)
#     try:
#         success = await order_service.update_order_state_by_id(order_id, current_user.role, order_dto)
#         if success:
#             return {"message": "Order completed successfully"}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

@router.patch("/orders/update/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["manager"]))], response_model=None)
async def update_order_as_completed(current_user: Annotated[User, Depends(get_current_user)], order_id: str, order_update: UpdateOrderDTO, session: AsyncSession = Depends(database.get_session)):
    repo = OrderRepository(session)
    repoI = InventoryRepository(session)
    inventory_service = GetInventoryByIdService(repoI)
    inventory_update_service = UpdateInventoryService(repoI)
    order_service = UpdateOrderStateByIdService(repo, inventory_service, inventory_update_service)
    try:
        success = await order_service.update_order_state_by_id(order_id, current_user.role, order_update,)
        if success:
            return {"message": "Order completed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/orders/cancel/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["manager"]))], response_model=None)
async def update_order_as_canceled(current_user: Annotated[User, Depends(get_current_user)], order_id: str, order_update: UpdateOrderDTO, session: AsyncSession = Depends(database.get_session)):
    repo = OrderRepository(session)
    order_service = CancelOrderService(repo)
    try:
        success = await order_service.cancel_order(order_id, current_user.id, current_user.role, order_update)
        if success:
            return {"message": "Order canceled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
