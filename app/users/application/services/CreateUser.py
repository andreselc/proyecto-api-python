from app.users.domain.port.IUserRepository import IUserRepository 
from app.users.application.dtos.CreateUserDto import CreateUserDto
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.users.auth.auth import get_password_hash


class CreateUser:
    def __init__(self, repo: IUserRepository[AggregateUser]):
        self.repo = repo

    async def create_user(self, user_dto: CreateUserDto) -> bool:
        username = await self.repo.IsExistUserName(user_dto.username)
        email = await self.repo.IsExistEmail(user_dto.email)

        if(user_dto.role.lower() == "superadmin"):
            raise ValueError(f"No puedes crear un usuario superadmin")
        
        if username is not None:
            raise ValueError(f"el nombre de usuario {user_dto.username} ya existe")

        if email is not None:
            raise ValueError(f"el correo {user_dto.email} ya esta registrado")

      
        user = AggregateUser.create(
            name = user_dto.name,
            email= user_dto.email,
            username= user_dto.username,
            password= get_password_hash(user_dto.password),
            role= user_dto.role
        )
        
        await self.repo.create_user(user)
        return True
    