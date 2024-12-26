from pydantic import BaseModel
from uuid import UUID

class InventoryDto(BaseModel):
    id: UUID
    quantity: int
    productCode: str
    productName: str
    productStatus: str