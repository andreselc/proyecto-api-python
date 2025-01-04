from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from app.users.infrastructure.db.database import get_session
from app.users.application.services.CreateUser import CreateUser as CreateUserService
from app.users.application.services.LoginUser import LoginUser as LoginUserService
from app.users.application.services.GetUsers import GetUsers as GetUsersService
from app.users.application.services.GetUserById import GetUserById as GetUserByIdService
from app.users.application.services.DeleteUser import DeleteUser as DeleteUserService
from app.users.application.services.UpdateUser import UpdateUser as UpdateUserService
from app.users.application.dtos.CreateUserDto import CreateUserDto
from app.users.application.dtos.UpdateUserDto import UpdateUserDto
from app.common.infrastructure.Modelo import User
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
         

@router.get("/users/all",status_code=status.HTTP_200_OK,dependencies=[Depends(RoleChecker(["superadmin"]))]) 
async def get_users(session: AsyncSession = Depends(get_session), role: str = Query(None, description="Filter by role (manager-customer-superadmin)")):
    repo = UserRepository(session)
    user_service =GetUsersService(repo)
    respuesta = await user_service.list_users(role)
    return respuesta

@router.get("/users/{user_id}",status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["superadmin"]))]) 
async def get_user_by_id(user_id:str,session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    user_service =GetUserByIdService(repo)
    try:
        respuesta = await user_service.get_user_by_id(user_id, True)
        return respuesta
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))    

@router.delete("/users/{user_id}",status_code=status.HTTP_200_OK,  dependencies=[Depends(RoleChecker(["superadmin"]))]) 
async def delete_user(user_id:str,session: AsyncSession = Depends(get_session)):

    repo = UserRepository(session)
    user_service =DeleteUserService(repo)
    success = await user_service.delete_user_id(user_id)
    if(success):
        return {"message": "User deleted successfully"}
      

@router.patch("/users/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(RoleChecker(["superadmin"]))], description="""
Fill in the fields you want to update. Leave the fields you don't want to change empty.

Example request body:
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "password": ""
}
""")
async def update_user(user_id:str, user_update: UpdateUserDto,session: AsyncSession = Depends(get_session)):
    pass
    repo = UserRepository(session)
    user_service =UpdateUserService(repo)
    try:
        success= await user_service.update_user(user_id, user_update)
        if(success):
            return {"message": "User updated successfully"}
    except ValueError as e:
         raise HTTPException(status_code=400, detail=str(e))   

@router.get("/users/get/me") 
async def get_me_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
