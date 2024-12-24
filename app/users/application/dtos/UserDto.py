from datetime import datetime
from pydantic import BaseModel

class UserDto(BaseModel):

    id: str
    name: str 
    email: str 
    username: str 
    role: str
    createdAt: datetime 
    updatedAt: datetime | None 

