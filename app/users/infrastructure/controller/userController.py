from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.users.infrastructure.db.database import get_session
from app.users.application.services.CreateUser import CreateUser as CreateUserServices
from app.users.application.dtos.CreateUserDto import CreateUserDto  
from app.users.infrastructure.repository.UserRepository import UserRepository

router = APIRouter()

@router.post("/users/register",tags=["Usuarios"], status_code=status.HTTP_201_CREATED) 
async def create_user(user_create: CreateUserDto, session: AsyncSession = Depends(get_session)):
    if(user_create.role.lower() == "superadmin"):
        raise HTTPException(status_code=400, detail="You can't create an superadmin user")
    else:
        repo = UserRepository(session)
        user_service = CreateUserServices(repo)
        success = await user_service.create_user(user_create)
        if(success):
            return {"message": "User created successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to create user")