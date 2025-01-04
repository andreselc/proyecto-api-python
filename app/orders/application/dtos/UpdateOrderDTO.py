from pydantic import BaseModel

class UpdateOrderDto(BaseModel):

    status: str