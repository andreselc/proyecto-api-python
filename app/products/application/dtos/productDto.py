from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ProductDto(BaseModel):
    id: UUID
    name: str
    code: str
    description: Optional[str] = None
    price: float
    status: str