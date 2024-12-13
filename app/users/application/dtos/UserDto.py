from datetime import datetime
from app.users.domain.userAgreggates.Enums.roleEnum import Role
from pydantic import BaseModel

class UserDto(BaseModel):

    id: str
    name: str 
    email: str 
    username: str 
    password: str 
    role: Role
    createdAt: datetime 
    updatedAt: datetime | None 

