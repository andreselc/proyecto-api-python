from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional


class UpdateUserDto(BaseModel):
    email: Optional[str] = Field(None, description="El correo del usuario", example="correo@gmail.com")
    username: Optional[str]  = Field(None, description="El nombre de usuario", example="johndoe")
    password: Optional[str]  = Field(None, description="La contraseña del usuario (min 7 caracteres)", example="password")
 
    @field_validator('email')
    def validate_email(cls, value):
        if value is None or value == "":
            return value  # Permitir que el email sea None o una cadena vacía
        # Expresión regular para validar el formato del correo electrónico
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValueError('El formato del correo electrónico es inválido.')
        return value

