from pydantic import BaseModel
from typing import Optional

class AddShoppiCartDto(BaseModel):
    quantity: int
    product_id: str