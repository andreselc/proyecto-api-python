from app.shopping_cart.infrastructure.model.shoppinCartModel import ShoppinCartModel
from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate

def aggregate_to_model(shoppin_cart: ShoppinCartAggregate, inventory_id: str) -> ShoppinCartAggregate:
    return ShoppinCartModel(
        id=shoppin_cart.shoppin_cart.id.get(),
        quantity=shoppin_cart.shoppin_cart.quantity.get(),
        inventory_id=inventory_id,
        user_id=shoppin_cart.user.id.get()
    )