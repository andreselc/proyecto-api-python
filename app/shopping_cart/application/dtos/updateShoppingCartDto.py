from pydantic import BaseModel
from typing import Optional

class UpdateInventoryDto(BaseModel):
    quantity: int
    