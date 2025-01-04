from datetime import datetime
from pydantic import BaseModel

class UserDto(BaseModel):

    id: str
    status: str
    totalprice: float
    createdAt: datetime 
    updatedAt: datetime | None 