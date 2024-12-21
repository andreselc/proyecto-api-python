from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.products.application.services.createProduct import CreateProductService
from app.products.application.services.getProducts import GetProductsService
from app.products.application.services.getProductById import GetProductByIdService
from app.products.application.dtos.createProductDto import CreateProductDto
from app.products.application.dtos.updateProductDto import UpdateProductDto
from app.products.application.services.deleteProduct import DeleteProductService
from app.products.application.services.updateProduct import UpdateProductService
from app.products.infrastructure.repository.productRepository import ProductRepository
from app.products.infrastructure.repository import database

router = APIRouter(
    tags=["Products"]
)

@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(product_dto: CreateProductDto, session: AsyncSession = Depends(database.get_session)):
    repo = ProductRepository(session)
    product_service = CreateProductService(repo)
    try:
        success = await product_service.create_product(product_dto)
        if success:
            return {"message": "Product created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
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

@router.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: str, session: AsyncSession = Depends(database.get_session)):
    repo = ProductRepository(session)
    product_service = DeleteProductService(repo)
    try:
        await product_service.delete_product(product_id)
        return {"message": "Product deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.patch("/products/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product_id: str, product_dto: UpdateProductDto, session: AsyncSession = Depends(database.get_session)):
    repo = ProductRepository(session)
    product_service = UpdateProductService(repo)
    try:
        success = await product_service.update_product(product_id, product_dto)
        if success:
            return {"message": "Product updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    