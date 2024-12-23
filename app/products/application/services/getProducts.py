from app.products.domain.ports.IProductRepository import IProductRepository
from app.products.domain.aggregate_root import ProductAggregate

class GetProductsService:
    def __init__(self, repo: IProductRepository[ProductAggregate]):
        self.repo = repo

    async def list_products(self) -> list[ProductAggregate]:
        return await self.repo.get_products()