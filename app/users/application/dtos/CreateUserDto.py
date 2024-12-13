from pydantic import BaseModel, Field, field_validator
from app.users.domain.userAgreggates.Enums.roleEnum import Role
import re

class CreateUserDto(BaseModel):
    
    name: str = Field(..., description="El nombre del usuario", example="John")
    email: str = Field(..., description="El correo del usuario", example="correo@gmail.com")
    username: str = Field(..., description="El nombre de usuario", example="johndoe")
    password: str = Field(..., description="La contraseña del usuario", example="password")
    role: Role = Field(..., description="Rol del usuario (superadmin, manager, custumer) - siempre en minuscula", example="password")

    @field_validator('email')
    def validate_email(cls, value):
        if value is None or value == "":
            raise ValueError('El correo electrónico es requerido.')
        # Expresión regular para validar el formato del correo electrónico
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValueError('El formato del correo electrónico es inválido.')
        return value
