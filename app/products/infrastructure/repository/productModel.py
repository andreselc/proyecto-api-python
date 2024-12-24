from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import uuid4
from datetime import datetime

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