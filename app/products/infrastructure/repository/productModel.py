from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import uuid4
from datetime import datetime

class Product(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    code: str
    status: str
    description: Optional[str] = None
    profit_margin: float
    cost: float
    price: float
    created_at: datetime = Field(default_factory=datetime.timestamp)
    updated_at: Optional[datetime] = Field(default=None)