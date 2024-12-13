from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import uuid4
from app.users.domain.userAgreggates.Enums.roleEnum import Role
    
class User(SQLModel, table=True):
    __tablename__ = "User"
    id: str = Field(default= lambda: str(uuid4()), primary_key=True)
    name: str 
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    password: str 
    role: Role 
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    updated_at: Optional[datetime] = Field(default=None)

