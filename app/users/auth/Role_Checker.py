#auth.py  
from typing import Annotated  
from fastapi import Depends, HTTPException, status  
from app.common.infrastructure.Modelo import User
from app.users.auth.auth import get_current_user
  
class RoleChecker:  
  def __init__(self, allowed_roles):  
    self.allowed_roles = allowed_roles  
  
  def __call__(self, user_dto: Annotated[User, Depends(get_current_user)]):  
    if user_dto.role in self.allowed_roles:  
      return True  
    allowed_roles_str = ", ".join(self.allowed_roles) 
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You don't have enough permissions. Allowed roles: {allowed_roles_str}")  
