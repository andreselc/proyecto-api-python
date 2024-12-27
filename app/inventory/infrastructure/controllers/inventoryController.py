from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.inventory.infrastructure.repository.inventoryRepository import InventoryRepository
from app.inventory.application.dtos.createInventoryDto import CreateInventoryDto
from app.inventory.application.dtos.updateInventoryDto import UpdateInventoryDto
from app.inventory.application.services.createInventory import CreateInventoryService
from app.inventory.application.services.updateInventory import UpdateInventoryService
from app.inventory.application.services.getInventoryById import GetInventoryByIdService

from app.products.application.services.getProductById import GetProductByIdService
from app.products.infrastructure.repository.productRepository import ProductRepository
from app.users.auth.Role_Checker import RoleChecker
from app.users.auth.auth import get_current_user
from app.inventory.infrastructure.mappers.domain_to_dto import domain_to_dto
from app.inventory.infrastructure.db import database

router = APIRouter(
    tags=["Inventory"]
)

@router.post("/inventory", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleChecker(["manager"]))])
async def create_inventory(inventory_dto: CreateInventoryDto, session: AsyncSession = Depends(database.get_session)):
    repo = InventoryRepository(session) #repositorio para inventario
    inventory_service = CreateInventoryService(repo)
    #repoP = ProductRepository(session) #repositorio para productos
    #product_service = GetProductByIdService(repoP)
    try:
        #product_aggregate = await product_service.get_product_by_id(inventory_dto.product_id)
        inventory_aggregate = await inventory_service.create_inventory(inventory_dto)
        inventory_dto = domain_to_dto(inventory_aggregate)
        return {"message": "Inventory assigned to product successfuly"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/inventories/{inventory_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["manager"]))])
async def get_inventory_by_id(inventory_id: str, session: AsyncSession = Depends(database.get_session)):
    repo = InventoryRepository(session)
    inventory_service = GetInventoryByIdService(repo)
    try:
        inventory_aggregate = await inventory_service.get_inventory_by_id(inventory_id)
        return domain_to_dto(inventory_aggregate)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.patch("inventories/{inventory_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["manager"]))])
async def update_inventory(inventory_id: str, inventory_dto: UpdateInventoryDto, session: AsyncSession = Depends(database.get_session)):
    repo = InventoryRepository(session)
    inventory_service = UpdateInventoryService(repo)
    try:
        success = await inventory_service.update_inventory(inventory_id, inventory_dto)
        if success:
            return {"message": "Inventory updated successfuly"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))