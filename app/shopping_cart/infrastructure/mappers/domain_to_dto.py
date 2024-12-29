from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate
from app.shopping_cart.application.dtos.shoppingCartDto import ShoppinCartDto

def domain_to_dto(shoppin_cart_aggregate: ShoppinCartAggregate) -> ShoppinCartDto:
    shoppin_cart, product, user = shoppin_cart_aggregate.get()
    return ShoppinCartDto(
        user_name=user.name.get(),
        shoppin_cart_id=shoppin_cart.id.get(),
        quantity=shoppin_cart.quantity.get(),
        product_id=product.id.get(),
        product_name=product.name.get(),
        product_code=product.code.get(),
        product_price=product.price.get(),
        product_status=product.status.value
    )