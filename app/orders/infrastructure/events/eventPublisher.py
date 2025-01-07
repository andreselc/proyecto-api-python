import asyncio

class EventPublisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    async def publish(self, event):
        tasks = [asyncio.create_task(subscriber(event)) for subscriber in self.subscribers]
        await asyncio.gather(*tasks)