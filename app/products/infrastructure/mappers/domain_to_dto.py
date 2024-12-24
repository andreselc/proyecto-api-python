from app.products.domain.aggregate_root import ProductAggregate
from app.products.application.dtos.productDto import ProductDto

def domain_to_dto(product_aggregate: ProductAggregate) -> ProductDto:
    product = product_aggregate.get()
    return ProductDto(
        id=product.id.get(),
        name=product.name.get(),
        code=product.code.get(),
        description=product.description.get(),
        price=product.price.get(),
        status=product.status.value
    )