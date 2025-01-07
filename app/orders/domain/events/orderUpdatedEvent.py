class OrderUpdatedEvent:
    def __init__(self, status: str, order_id: str, username: str):
        self.order_id = order_id
        self.username = username
        self.status = status
        self.message = f"Usuario {username}, su orden con ID {order_id} ha sido actualizada a {status}."