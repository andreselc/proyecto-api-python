from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from app.users.infrastructure.db.database import get_session
from app.users.application.services.CreateUser import CreateUser as CreateUserService
from app.users.application.services.LoginUser import LoginUser as LoginUserService
from app.users.application.services.GetUsers import GetUsers as GetUsersService
from app.users.application.services.GetUserMe import GetUserMe as GetUserMeService
from app.users.application.dtos.CreateUserDto import CreateUserDto
from app.users.application.dtos.LoginUserDto import LoginUserDto
from app.users.application.dtos.UserDto import UserDto
from app.users.infrastructure.model.ModelUser import User
from app.users.infrastructure.repository.UserRepository import UserRepository

from app.users.auth.auth import get_current_user
from app.users.auth.Role_Checker import RoleChecker
from fastapi.security import  OAuth2PasswordRequestForm

router = APIRouter(tags=["Usuarios"])

@router.post("/users/register", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleChecker(["superadmin"]))]) 
async def create_user(user_create: CreateUserDto, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    user_service = CreateUserService(repo)
    try:
        success = await user_service.create_user(user_create)
        if(success):
            return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))    
        
@router.post("/users/login") 
async def login(user_login: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    user_service =LoginUserService(repo)
    respuesta = await user_service.loginuser(user_login)
    return respuesta 
         

@router.get("/users/all",dependencies=[Depends(RoleChecker(["superadmin"]))]) 
async def get_users(session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    user_service =GetUsersService(repo)
    respuesta = await user_service.list_users()
    return respuesta

@router.get("/users/me") 
async def get_me_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user