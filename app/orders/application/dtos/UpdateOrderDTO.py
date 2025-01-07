from pydantic import BaseModel

class UpdateOrderDTO(BaseModel):
    status: str