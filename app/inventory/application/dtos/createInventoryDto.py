from pydantic import BaseModel
from typing import Optional

class CreateInventoryDto(BaseModel):
    quantity: int
    product_id: str
    name: str
    code: str
    description: Optional[str] = None
    profit_margin: float
    cost: float