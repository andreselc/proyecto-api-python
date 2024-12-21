from app.products.domain.ports.IProductRepository import IProductRepository
from app.products.domain.aggregate_root import ProductAggregate
from app.products.application.dtos.productDto import ProductDto
from app.products.infrastructure.mappers.domain_to_dto import domain_to_dto

class GetProductsService:
    def __init__(self, repo: IProductRepository[ProductAggregate]):
        self.repo = repo

    async def list_products(self) -> list[ProductDto]:
        product_aggregates = await self.repo.get_products()
        return [domain_to_dto(product) for product in product_aggregates]