from app.products.domain.ports.IProductRepository import IProductRepository
from app.products.application.dtos.createProductDto import CreateProductDto
from app.products.domain.aggregate_root import ProductAggregate

class CreateProductService:
    def __init__(self, repo: IProductRepository[ProductAggregate]):
        self.repo = repo

    async def create_product(self, product_dto: CreateProductDto) -> bool:
        product_aggregate = ProductAggregate.create(
            name=product_dto.name,
            code=product_dto.code,
            description=product_dto.description,
            margin_profit=product_dto.profit_margin,
            cost=product_dto.cost,
            status="active"
        )
        await self.repo.create_product(product_aggregate)
        return True  