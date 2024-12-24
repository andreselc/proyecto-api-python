from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import uuid4
from app.users.domain.enums.roleEnum import Role
    
class User(SQLModel, table=True):
    __tablename__ = "User"
    id: str = Field(default= lambda: str(uuid4()), primary_key=True)
    name: str 
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    password: str 
    role: Role 
    created_at: str = Field(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    updated_at: Optional[str] = Field(default=None)

