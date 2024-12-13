from app.users.domain.port import IUserRepository
from app.users.application.dtos import CreateUserDto
from app.users.infrastructure.model.ModelUser import User

class CreateUser:
    def __init__(self, repo: IUserRepository[User]):
        self.repo = repo

    async def create_user(self, user_dto: CreateUserDto):
        user = User(
            name = user_dto.name,
            email= user_dto.email,
            username= user_dto.username,
            password= user_dto.password,
            role= user_dto.role
        )
        
        return await self.repo.create_user(user)