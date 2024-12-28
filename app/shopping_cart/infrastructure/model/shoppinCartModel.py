from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from uuid import uuid4
from app.inventory.infrastructure.model.inventoryModel import InventoryModel
from app.users.infrastructure.model.ModelUser import User

class ShoppinCartModel(SQLModel, table = True):
    id: str = Field(default_factory=lambda: str(uuid4), primary_key=True)
    quantity: int
    inventory_id: str = Field(foreign_key="inventorymodel.id")
    user_id: str = Field(foreign_key="User.id")
    inventory: InventoryModel = Relationship(back_populates="shoppin_cart")
    user: User = Relationship(back_populates="shoppin_cart")
