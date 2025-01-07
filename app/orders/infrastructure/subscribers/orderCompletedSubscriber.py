import asyncio

class OrderCompletedSubscriber:
    async def handle_event(self, event):
        await asyncio.sleep(1)  # Simula el procesamiento del evento
        print(f"Orden completada: {event}")