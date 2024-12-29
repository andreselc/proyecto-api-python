from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.products.application.services.getProductById import GetProductByIdService
from app.users.application.services.GetUserById import GetUserById
from app.shopping_cart.application.services.addShoppinCartProduct import AddShoppinCartProductService
from app.shopping_cart.application.services.updateShoopinCartProduct import updateShoppinCartProductService
from app.shopping_cart.application.services.getShoppinCartProducts import GetShoppinCartProducts
from app.shopping_cart.application.services.getShoppinCartProductById import GetShoppinCartProductById

from app.shopping_cart.application.dtos.addShoppingCartDto import AddShoppiCartDto
from app.shopping_cart.application.dtos.updateShoppingCartDto import UpdateInventoryDto

from app.shopping_cart.infrastructure.repository.shoppinCartRepository import ShoppingCartRepository
from app.products.infrastructure.repository.productRepository import ProductRepository
from app.users.infrastructure.repository.UserRepository import UserRepository
from app.shopping_cart.infrastructure.db import database
from app.shopping_cart.infrastructure.mappers.domain_to_dto import domain_to_dto

router = APIRouter(
    tags=["Shopping Cart"]
)

@router.post("shopping_cart", status_code=status.HTTP_201_CREATED)
async def add_shopping_cart_product(shoppin_cart_dto: AddShoppiCartDto, session: AsyncSession = Depends(database.get_session)):
    repo = ShoppingCartRepository(session)
    shoppin_cart_service = AddShoppinCartProductService(repo)
    repoP = ProductRepository(session) #repositorio para producto
    product_service = GetProductByIdService(repoP)
    repoU = UserRepository(session) #repositorio para usuario
    user_service = GetUserById(repoU)

    try:
        product_aggregate = await product_service.get_product_by_id(shoppin_cart_dto.product_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/shopping_cart/all", status_code=status.HTTP_200_OK)
async def list_products_in_shopping_cart(session: AsyncSession = Depends(database.get_session)):
    repo = ShoppingCartRepository(session)
    shoppin_cart_service = GetShoppinCartProducts(repo)
    repoU = UserRepository(session) #repositorio para usuario
    user_service = GetUserById(repoU)
    try:
        user_aggregate = user_service.get_user_by_id() #hay que cambiar esta funcion por la de Alex
        shoppin_cart_aggregates = await shoppin_cart_service.get_shoppin_cart_products(user_aggregate.id)
        products = [domain_to_dto(shoppin_carts) for shoppin_carts in shoppin_cart_aggregates]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/shopping_cart/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_in_shopping_cart_by_id(session: AsyncSession = Depends(database.get_session)):
    repo = ShoppingCartRepository(session)
    shoppin_cart_service = GetShoppinCartProductById(repo)