from app.products.domain.ports.IProductRepository import IProductRepository
from app.products.application.dtos import createProductDto
from app.products.infrastructure.repository.productModel import Product

class CreateProductService:
    def __init__(self, repo: IProductRepository[Product]):
        self.repo = repo

    async def create_product(self, product_dto: createProductDto) -> None:
        product = Product(
            name=product_dto.name,
            code=product_dto.code,
            description=product_dto.description,
            profit_margin=product_dto.profit_margin,
            cost=product_dto.cost,
            price=product_dto.cost * (1 + product_dto.profit_margin / 100),
            status="active"
        )
        await self.repo.create_product(product)