from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UpdateProductDto(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    profit_margin: Optional[float] = None
    cost: Optional[float] = None