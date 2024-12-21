from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.products.application.services.createProduct import CreateProductService
from app.products.application.services.getProducts import GetProductsService
from app.products.application.services.getProductById import GetProductByIdService
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
    
@router.get("/products", status_code=status.HTTP_200_OK)
async def list_products(session: AsyncSession = Depends(database.get_session)):
    repo = ProductRepository(session)
    product_service = GetProductsService(repo)
    products = await product_service.list_products()
    return products

@router.get("/products/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(product_id: str, session: AsyncSession = Depends(database.get_session)):
    repo = ProductRepository(session)
    product_service = GetProductByIdService(repo)
    try:
        product = await product_service.get_product_by_id(product_id)
        return product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))