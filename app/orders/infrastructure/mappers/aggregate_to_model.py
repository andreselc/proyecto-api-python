from app.common.infrastructure.Modelo import OrderModel
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from datetime import datetime

def aggregate_to_model(order_aggregate: OrderAggregate) -> OrderModel:
    return OrderModel(
        id = order_aggregate.order.id.get(),
        status = order_aggregate.order.status.value,
        total_price = order_aggregate.order.totalprice.get(),
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        user_id = order_aggregate.user.id.get()
    )