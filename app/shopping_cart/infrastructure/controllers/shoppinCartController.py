from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.products.application.services.getProductById import GetProductByIdService
from app.users.application.services.GetUserById import GetUserById
from app.shopping_cart.application.services.addShoppinCartProduct import AddShoppinCartProductService
from app.shopping_cart.application.services.updateShoopinCartProduct import updateShoppinCartProductService
from app.shopping_cart.application.services.getShoppinCartProducts import GetShoppinCartProducts
from app.shopping_cart.application.services.getShoppinCartProductById import GetShoppinCartProductById
from app.inventory.application.services.getInventoryByProductId import GetInventoryByProductIdService
from app.shopping_cart.application.services.deleteShoppinCartProduct import DeleteShoppinCartProductService

from app.shopping_cart.application.dtos.addShoppingCartDto import AddShoppiCartDto
from app.shopping_cart.application.dtos.updateShoppingCartDto import UpdateInventoryDto

from app.shopping_cart.infrastructure.repository.shoppinCartRepository import ShoppingCartRepository
from app.products.infrastructure.repository.productRepository import ProductRepository
from app.users.infrastructure.repository.UserRepository import UserRepository
from app.inventory.infrastructure.repository.inventoryRepository import InventoryRepository

from app.shopping_cart.infrastructure.db import database
from app.shopping_cart.infrastructure.mappers.domain_to_dto import domain_to_dto
from app.users.auth.auth import get_current_user
from app.common.infrastructure.Modelo import User

router = APIRouter(
    tags=["Shopping Cart"]
)

@router.post("/shopping_cart", status_code=status.HTTP_201_CREATED)
async def add_shopping_cart_product(shoppin_cart_dto: AddShoppiCartDto, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(database.get_session)):
    repo = ShoppingCartRepository(session)
    shoppin_cart_service = AddShoppinCartProductService(repo)
    repoP = ProductRepository(session) #repositorio para producto
    product_service = GetProductByIdService(repoP)
    repoU = UserRepository(session) #repositorio para usuario
    user_service = GetUserById(repoU)
    repoI = InventoryRepository(session) #repositorio para inventario
    inventory_service = GetInventoryByProductIdService(repoI)
    try:
        product_aggregate = await product_service.get_product_by_id(shoppin_cart_dto.product_id)
        inventory_aggregate = await inventory_service.get_inventory_by_product_id(shoppin_cart_dto.product_id)
        user_aggregate = await user_service.get_user_by_id(current_user.id, False)
        shoppin_cart_service = await shoppin_cart_service.add_shoppin_cart_product(shoppin_cart_dto, product_aggregate, user_aggregate, inventory_aggregate)
        return {"message": "Product added to shopping cart successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/shopping_cart/all", status_code=status.HTTP_200_OK)
async def list_products_in_shopping_cart(current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(database.get_session)):
    #falta arreglar esto en el domain_to_dto
    repo = ShoppingCartRepository(session)
    shoppin_cart_service = GetShoppinCartProducts(repo)
    try:
        shoppin_cart_aggregates = await shoppin_cart_service.get_shoppin_cart_products(current_user.id)
        products = [domain_to_dto(shoppin_carts) for shoppin_carts in shoppin_cart_aggregates]
        return products
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/shopping_cart/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_in_shopping_cart_by_id(product_id: str, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(database.get_session)):
    repo = ShoppingCartRepository(session)
    shoppin_cart_service = GetShoppinCartProductById(repo)
    repoI = InventoryRepository(session) #repositorio para inventario
    inventory_service = GetInventoryByProductIdService(repoI)
    try:
        inventory_aggregate = await inventory_service.get_inventory_by_product_id(product_id)
        shoppin_cart_aggregate = await shoppin_cart_service.get_shoppin_cart_product_by_id(inventory_aggregate.inventory.id.get(), current_user.id, product_id)
        return domain_to_dto(shoppin_cart_aggregate)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/shopping_cart/delete/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product_in_shopping_cart(product_id: str, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(database.get_session)):
    repo = ShoppingCartRepository(session)
    shoppin_cart_service = DeleteShoppinCartProductService(repo)
    repoI = InventoryRepository(session)
    inventory_service = GetInventoryByProductIdService(repoI)
    try:
        inventory_aggregate = await inventory_service.get_inventory_by_product_id(product_id)
        await shoppin_cart_service.delete_shoppin_cart_product(inventory_aggregate.inventory.id.get(), current_user.id, product_id)
        return {"message": "Product deleted from shopping cart successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.patch("/shopping_cart/update/{product_id}", status_code=status.HTTP_200_OK)
async def update_product_in_shopping_cart(product_id: str, shoppin_cart_dto: UpdateInventoryDto, current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(database.get_session)):
    repo = ShoppingCartRepository(session)
    shoppin_cart_service = updateShoppinCartProductService(repo)
    repoI = InventoryRepository(session)
    inventory_service = GetInventoryByProductIdService(repoI)
    try:
        inventory_aggregate = await inventory_service.get_inventory_by_product_id(product_id)
        await shoppin_cart_service.update_shoppin_cart_product(inventory_aggregate.inventory.id.get(), current_user.id, product_id, shoppin_cart_dto)
        return {"message": "Product updated in shopping cart successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

