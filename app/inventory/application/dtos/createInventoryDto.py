from pydantic import BaseModel
from typing import Optional

class CreateInventoryDto(BaseModel):
    quantity: int
    product_id: str