from pydantic import BaseModel

class LoginRespuestaUserDto(BaseModel):
    access_token: str
    token_type: str
    
