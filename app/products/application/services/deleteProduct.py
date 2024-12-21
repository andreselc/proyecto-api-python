from app.products.domain.ports.IProductRepository import IProductRepository
from app.products.domain.aggregate_root import ProductAggregate

class DeleteProductService:
    def __init__(self, repo: IProductRepository[ProductAggregate]):
        self.repo = repo

    async def delete_product(self, product_id: str) -> bool:
        product_aggregate = await self.repo.get_product_by_id(product_id)
        if not product_aggregate:
            raise ValueError(f"Product with id {product_id} not found")
        await self.repo.delete_product(product_id)
        return True