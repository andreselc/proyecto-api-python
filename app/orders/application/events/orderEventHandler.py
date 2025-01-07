import asyncio
from app.orders.domain.events.orderUpdatedEvent import OrderUpdatedEvent

class OrderUpdatedEventHandler:
    def __init__(self):
        self.event_queue = asyncio.Queue()  # Cola de eventos

    async def publish_event(self, event: OrderUpdatedEvent):
        await self.event_queue.put(event)
        print(f"Evento publicado")

    async def consume_events(self):
        while not self.event_queue.empty():
            event = await self.event_queue.get()
            await self.handle_event(event)

    async def handle_event(self, event: OrderUpdatedEvent):
        # Simular tiempo de procesamiento
        await asyncio.sleep(2)  # Esperar 2 segundos
        # Manejo del evento, como enviar una notificación
        print(f"Notificación: {event.message}")