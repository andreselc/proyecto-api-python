from app.orders.application.dtos.UpdateOrderDTO import UpdateOrderDTO
from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.orders.domain.events.orderUpdatedEvent import OrderUpdatedEvent
from app.orders.application.events.orderEventHandler import OrderUpdatedEventHandler
from app.inventory.application.services.getInventoryById import GetInventoryByIdService
from app.inventory.application.services.updateInventory import UpdateInventoryService
from app.inventory.application.dtos.updateInventoryDto import UpdateInventoryDto

class CancelOrderService:
    def __init__(self, repo: IOrderRepository[OrderAggregate], event_handler: OrderUpdatedEventHandler, inventory_service: GetInventoryByIdService, inventory_update_service: UpdateInventoryService):
        self.repo = repo
        self.event_handler = event_handler
        self.inventory_service = inventory_service
        self.inventory_update_service = inventory_update_service

    async def cancel_order(self, order_id: str, user_id: str, user_role: str, orderDTO: UpdateOrderDTO) -> bool:
        order_aggregate = await self.repo.get_order_by_id(order_id)
        if not order_aggregate:
            raise ValueError(f"Order with id {order_id} not found")
        
        print("Antes de cancelar: ", order_aggregate.order.status.value)

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

        if order_aggregate.order.status.value == "completed":
            order_items = await self.repo.get_order_items(order_id)
        for inventory_id, quantity in order_items:
            inventory_aggregate = await self.inventory_service.get_inventory_by_id(inventory_id)
            new_quantity = inventory_aggregate.inventory.quantity.get() + quantity  # Revertir la cantidad

            update_inventory_dto = UpdateInventoryDto(
                quantity=new_quantity
            )
            await self.inventory_update_service.update_inventory(inventory_aggregate.id.get(), update_inventory_dto)


        order_aggregate_evento = await self.repo.get_order_by_id(order_id)
        print("Despues de cancelar: ", order_aggregate_evento.order.status.value)

        # Publicar el evento de dominio
        event = OrderUpdatedEvent(status=order_aggregate_evento.order.status.value, order_id=order_aggregate_evento.id.get(), username=order_aggregate_evento.user.username.get())
        await self.event_handler.publish_event(event)

        # Consumir eventos
        await self.event_handler.consume_events()

        return True