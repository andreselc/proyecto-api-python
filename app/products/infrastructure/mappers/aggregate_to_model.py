from app.common.infrastructure.Modelo import ProductModel
from app.products.domain.aggregate_root import ProductAggregate
from datetime import datetime, timezone

def aggregate_to_model(product_aggregate: ProductAggregate) -> ProductModel:
    return ProductModel(
        id=product_aggregate.product.id.get(),
        name=product_aggregate.product.name.get(),
        code=product_aggregate.product.code.get(),
        description=product_aggregate.product.description.get(),
        profit_margin=product_aggregate.product.margin_profit.get(),
        cost=product_aggregate.product.cost.get(),
        price=product_aggregate.product.price.get(),
        status=product_aggregate.product.status.value,
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    )