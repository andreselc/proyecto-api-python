from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.products.application.services.createProduct import CreateProductService
from app.products.application.dtos.createProductDto import CreateProductDto
from app.products.infrastructure.repository.productRepository import ProductRepository
from app.products.infrastructure.repository import database

router = APIRouter()

@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(product_dto: CreateProductDto, session: AsyncSession = Depends(database.get_session)):
    repo = ProductRepository(session)
    product_service = CreateProductService(repo)
    success = await product_service.create_product(product_dto)
    if success:
        return {"message": "Product created successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to create product")