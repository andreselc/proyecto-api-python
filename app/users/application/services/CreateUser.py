from app.users.domain.port.IUserRepository import IUserRepository 
from app.users.application.dtos.CreateUserDto import CreateUserDto
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.users.seguridad.auth import get_password_hash

class CreateUser:
    def __init__(self, repo: IUserRepository[AggregateUser]):
        self.repo = repo

    async def create_user(self, user_dto: CreateUserDto) -> bool:
        user = AggregateUser.create(
            name = user_dto.name,
            email= user_dto.email,
            username= user_dto.username,
            password= get_password_hash(user_dto.password),
            role= user_dto.role
        )
        
        await self.repo.create_user(user)
        return True
    