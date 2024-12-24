from app.products.domain.ports.IProductRepository import IProductRepository
from app.products.domain.aggregate_root import ProductAggregate
from app.products.application.dtos.updateProductDto import UpdateProductDto

class UpdateProductService:
    def __init__(self, repo: IProductRepository[ProductAggregate]):
        self.repo = repo

    async def update_product(self, product_id: str, product_dto: UpdateProductDto) -> bool:
        product_aggregate = await self.repo.get_product_by_id(product_id)
        if not product_aggregate:
            raise ValueError(f"Product with id {product_id} not found")

        existing_products = await self.repo.get_products()
        for product in existing_products:
            if product.product.code.get() == product_dto.code and product.product.id != product_id:
                raise ValueError(f"Product with code {product_dto.code} already exists")

        product_aggregate.update(
            name=product_dto.name,
            code=product_dto.code,
            description=product_dto.description,
            margin_profit=product_dto.profit_margin,
            cost=product_dto.cost,
            status=product_dto.status
        )
        await self.repo.update_product(product_aggregate)
        return True