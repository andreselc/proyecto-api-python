from pydantic import BaseModel
from typing import Optional

class UpdateInventoryDto(BaseModel):
    quantity: int
    name: str
    code: str
    description: Optional[str] = None
    profit_margin: float
    cost: float