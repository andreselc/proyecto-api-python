from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CreateProductDto(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    profit_margin: float
    cost: float