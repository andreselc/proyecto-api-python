from app.common.infrastructure.Modelo import User
from app.users.application.dtos.UserDto import UserDto

def model_to_dto(user: User) -> UserDto:
    return UserDto(
        id= user.id,
        name = user.name, 
        email= user.email, 
        username= user.username, 
        role= user.role,
        createdAt= user.created_at,
        updatedAt= user.updated_at 
    )
    