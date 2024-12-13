from fastapi import APIRouter, HTTPException, Depends, status

router = APIRouter()


@router.post("/users/register",tags=["Usuarios"]) 
def create_user():
    return {"message": "User created successfully"}