from app.products.domain.ports.IProductRepository import IProductRepository
from app.products.domain.aggregate_root import ProductAggregate

class GetProductByIdService:
    def __init__(self, repo: IProductRepository[ProductAggregate]):
        self.repo = repo

    async def get_product_by_id(self, product_id: str) -> ProductAggregate:
        product_aggregate = await self.repo.get_product_by_id(product_id)
        if not product_aggregate:
            raise ValueError(f"Product with id {product_id} not found")
        return product_aggregate