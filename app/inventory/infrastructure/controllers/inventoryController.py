from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.inventory.application.dtos.createInventoryDto import CreateInventoryDto
from app.inventory.application.dtos.updateInventoryDto import UpdateInventoryDto
from app.inventory.application.dtos.inventoryDto import Inventory
from app.inventory.application.services.createInventory import CreateInventoryService
from app.inventory.application.services.updateInventory import UpdateInventoryService
from app.inventory.application.services.getInventoryById import GetInventoryByIdService
from app.users.auth.Role_Checker import RoleChecker
from app.users.auth.auth import get_current_user
from app.inventory.infrastructure.db import database

router = APIRouter(
    tags=["Inventory"]
)

@router.post("/inventory", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleChecker(["manager"]))])
async def create_inventory(inventory_dto: CreateInventoryDto, session: AsyncSession = Depends(database.get_session)):
    pass

