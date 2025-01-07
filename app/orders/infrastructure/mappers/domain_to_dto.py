# application/mappers/domain_to_dto.py
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.orders.application.dtos.OrderDTO import OrderDto
from datetime import datetime

def domain_to_dto(order_aggregate: OrderAggregate) -> OrderDto:
    order, products, user = order_aggregate.get()
    return OrderDto(
        id=order.id.get(),
        status=order.status.value,
        totalprice=order.totalprice.get(),
        createdAt=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )