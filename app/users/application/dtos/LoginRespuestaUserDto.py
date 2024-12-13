from pydantic import BaseModel

class LoginRespuestaUserDto(BaseModel):
    id: str 
    name: str 
    username: str 
    token: str
    
