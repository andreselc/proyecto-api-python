from app.orders.application.dtos.UpdateOrderDTO import UpdateOrderDTO
from app.orders.domain.ports.IOrderRepository import IOrderRepository
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.orders.domain.events.orderUpdatedEvent import OrderUpdatedEvent
from app.orders.application.events.orderEventHandler import OrderUpdatedEventHandler
from app.inventory.application.services.getInventoryById import GetInventoryByIdService
from app.inventory.application.services.updateInventory import UpdateInventoryService
from app.common.infrastructure.Modelo import OrderItem
from app.orders.infrastructure.mappers.aggregate_to_model_OrderItem import aggregate_to_model_order_item
from app.inventory.application.dtos.updateInventoryDto import UpdateInventoryDto

class UpdateOrderStateByIdService:
    def __init__(self, repo: IOrderRepository[OrderAggregate], inventory_service: GetInventoryByIdService, inventory_update_service: UpdateInventoryService, event_handler: OrderUpdatedEventHandler):
        self.repo = repo
        self.inventory_service = inventory_service
        self.inventory_update_service = inventory_update_service
        self.event_handler = event_handler

    async def update_order_state_by_id(self, order_id: str, user_role: str, orderDTO: UpdateOrderDTO) -> bool:
        order_aggregate = await self.repo.get_order_by_id(order_id)

        if not order_aggregate:
            raise ValueError(f"Order with id {order_id} not found")
        
        print("Antes de actualizar: ",order_aggregate.order.status.value)
        
        # Verificar que el usuario tiene el rol de manager
        if user_role != "manager":
            raise PermissionError("Only managers can update the order status to completed")

        order_aggregate.update(
            status="completed"
        )

        await self.repo.update_order_state_by_id(order_aggregate)

        order_aggregate_evento = await self.repo.get_order_by_id(order_id)
        print("Despues de actualizar: ",order_aggregate_evento.order.status.value)
        
        order_items = await self.repo.get_order_items(order_id)
        for inventory_id, quantity in order_items:
            inventory_aggregate = await self.inventory_service.get_inventory_by_id(inventory_id)
            new_quantity = inventory_aggregate.inventory.quantity.get() - quantity

            
            update_inventory_dto = UpdateInventoryDto(
                quantity=new_quantity
            )
            await self.inventory_update_service.update_inventory(inventory_aggregate.id.get(), update_inventory_dto)

    
        # Publicar el evento de dominio
        event = OrderUpdatedEvent(status=order_aggregate_evento.order.status.value, order_id=order_aggregate_evento.id.get(), username=order_aggregate_evento.user.username.get())
        await self.event_handler.publish_event(event)

        # Consumir eventos
        await self.event_handler.consume_events()

        return True