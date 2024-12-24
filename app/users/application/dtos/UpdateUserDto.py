from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional


class UpdateUserDto(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str]  = None
    password: Optional[str]  = None
 
    @field_validator('email')
    def validate_email(cls, value):
        if value is None or value == "":
            return None  # Permitir que el email sea None si no se proporciona
        # Expresión regular para validar el formato del correo electrónico
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValueError('Invalid email format')
        return value

