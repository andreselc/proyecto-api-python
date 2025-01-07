from app.orders.application.dtos.UpdateOrderDTO import UpdateOrderDTO
from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.orders.infrastructure.events.eventPublisher import EventPublisher
from app.orders.domain.events.orderCompletedEvent import OrderCompletedEvent
from app.inventory.application.services.getInventoryByProductId import GetInventoryByProductIdService
from app.common.infrastructure.Modelo import OrderItem
from app.orders.infrastructure.mappers.aggregate_to_model_OrderItem import aggregate_to_model_order_item

class UpdateOrderStateByIdService:
    def __init__(self, repo: IOrderRepository[OrderAggregate], inventory_service: GetInventoryByProductIdService):
        self.repo = repo
        self.inventory_service = inventory_service

    async def update_order_state_by_id(self, order_id: str, user_role: str, orderDTO: UpdateOrderDTO) -> bool:
        order_aggregate = await self.repo.get_order_by_id(order_id)
        print("Entre aqui 1")
        if not order_aggregate:
            raise ValueError(f"Order with id {order_id} not found")
        
        # Verificar que el usuario tiene el rol de manager
        if user_role != "manager":
            raise PermissionError("Only managers can update the order status to completed")

        order_aggregate.update(
            status=orderDTO.status
        )

        print("Entre aqui 2")

        await self.repo.update_order_state_by_id(order_aggregate)

        print("Entre aqui 3")

        # # Lanzar el evento de dominio
        # event = OrderCompletedEvent(order_id=order_id, user_id=order_aggregate.user_id, status="completed")
        # await self.event_publisher.publish(event)

        return True