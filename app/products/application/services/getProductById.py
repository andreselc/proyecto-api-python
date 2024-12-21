from app.products.domain.ports.IProductRepository import IProductRepository
from app.products.domain.aggregate_root import ProductAggregate
from app.products.application.dtos.productDto import ProductDto
from app.products.infrastructure.mappers.domain_to_dto import domain_to_dto

class GetProductByIdService:
    def __init__(self, repo: IProductRepository[ProductAggregate]):
        self.repo = repo

    async def get_product_by_id(self, product_id: str) -> ProductDto:
        product_aggregate = await self.repo.get_product_by_id(product_id)
        if not product_aggregate:
            raise ValueError(f"Product with id {product_id} not found")
        return domain_to_dto(product_aggregate)