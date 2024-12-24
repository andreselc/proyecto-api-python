from pydantic import BaseModel, Field

class LoginUserDto(BaseModel):
    username: str = Field(..., description="El nombre de usuario", example="johndoe")
    password: str = Field(..., description="La contraseña del usuario", example="password")
 

