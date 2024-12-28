from app.users.domain.port.IUserRepository import IUserRepository 
from app.users.application.dtos.CreateUserDto import CreateUserDto
from app.users.domain.aggregate.aggregate_user import AggregateUser
from uuid import uuid4

class CreateUser:
    def __init__(self, repo: IUserRepository[AggregateUser]):
        self.repo = repo

    async def create_user(self, user_dto: CreateUserDto) -> bool:
        username = await self.repo.IsExistUserName(user_dto.username)
        email = await self.repo.IsExistEmail(user_dto.email)

        if(user_dto.role.lower() == "superadmin"):
            raise ValueError(f"You can't create a superadmin user")
        
        if username is not None:
            raise ValueError(f"The username {user_dto.username} is already registered")

        if email is not None:
            raise ValueError(f"The email {user_dto.email} is already registered")

      
        user = AggregateUser.create(
            id= str(uuid4()),
            name = user_dto.name,
            email= user_dto.email,
            username= user_dto.username,
            password= user_dto.password,
            role= user_dto.role
        )
        
        await self.repo.create_user(user)
        return True
    