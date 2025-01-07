from app.orders.application.dtos.UpdateOrderDTO import UpdateOrderDTO
from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate

class CancelOrderService:
    def __init__(self, repo: IOrderRepository[OrderAggregate]):
        self.repo = repo

    async def cancel_order(self, order_id: str, user_id: str, user_role: str, orderDTO: UpdateOrderDTO) -> bool:
        order_aggregate = await self.repo.get_order_by_id(order_id)
        if not order_aggregate:
            raise ValueError(f"Order with id {order_id} not found")
        

        # Verificar que la orden pertenece al usuario logeado o que el usuario es un gerente
        if order_aggregate.user.id != user_id and user_role != "manager":
            raise PermissionError("You do not have permission to cancel this order")
        
        # Verificar que el cliente solo puede cancelar órdenes pendientes
        if user_role == "customer" and order_aggregate.status != "pending":
            raise ValueError("Customers can only cancel pending orders")
        

        order_aggregate.update(
            status=orderDTO.status
        )

        await self.repo.cancel_order(order_aggregate)
        return True