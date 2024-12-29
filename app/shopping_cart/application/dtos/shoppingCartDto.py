from pydantic import BaseModel
from uuid import UUID

class ShoppinCartDto(BaseModel):
    user_name: str
    shoppin_cart_id: UUID
    quantity: int
    product_id: UUID
    product_code: str
    product_name: str
    product_price: float
    product_status: str
