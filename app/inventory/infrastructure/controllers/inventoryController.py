from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.inventory.application.dtos.createInventoryDto import CreateInventoryDto
from app.inventory.application.dtos.updateInventoryDto import UpdateInventoryDto
from app.inventory.application.dtos.inventoryDto import Inventory

router = APIRouter(
    tags=["Inventory"]
)

