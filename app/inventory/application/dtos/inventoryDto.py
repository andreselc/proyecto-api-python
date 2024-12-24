from pydantic import BaseModel
from uuid import UUID

class Inventory(BaseModel):
    id: UUID
    quantity: int
    productCode: str