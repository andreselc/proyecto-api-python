from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import uuid4
from app.users.domain.enums.roleEnum import Role
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    __tablename__ = "User"
    id: str = Field(default_factory= lambda: str(uuid4()), primary_key=True)
    name: str 
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    password: str 
    role: Role 
    created_at: str = Field(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    updated_at: Optional[str] = Field(default=None)
    shoppin_cart: Optional["ShoppinCartModel"]= Relationship(back_populates="user")

class ProductModel(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    code: str
    status: str
    description: Optional[str] = None
    profit_margin: float
    cost: float
    price: float
    created_at: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at: Optional[str] = Field(default=None)

class InventoryModel(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    quantity: int
    created_at: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at: Optional[str] = Field(default=None)
    product_id: str = Field(default=None, foreign_key="productmodel.id")
    shoppin_cart: list["ShoppinCartModel"] = Relationship(back_populates="inventory") 

class ShoppinCartModel(SQLModel, table = True):
    id: str = Field(default_factory=lambda: str(uuid4), primary_key=True)
    quantity: int
    inventory_id: str = Field(foreign_key="inventorymodel.id", primary_key=True)
    user_id: str = Field(foreign_key="User.id", primary_key=True)
    inventory: InventoryModel = Relationship(back_populates="shoppin_cart")
    user: User = Relationship(back_populates="shoppin_cart")

#Agregar Modelo Orden 

