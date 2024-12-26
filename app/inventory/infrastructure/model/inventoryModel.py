from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from uuid import uuid4
from datetime import datetime
from app.products.infrastructure.repository.productModel import ProductModel

class InventoryModel(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    quantity: int
    created_at: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at: Optional[str] = Field(default=None)
    product_id: str = Field(default=None, foreign_key="productmodel.id")  