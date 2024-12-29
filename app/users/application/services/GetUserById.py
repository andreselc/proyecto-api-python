from app.users.domain.port.IUserRepository import IUserRepository 
from app.users.application.dtos.UserDto import UserDto
from app.users.domain.aggregate.aggregate_user import AggregateUser

class GetUserById:
    def __init__(self, repo: IUserRepository[AggregateUser]):
        self.repo = repo

    async def get_user_by_id(self, id: str, retornar_dto: bool) -> UserDto:
        user = await self.repo.get_user_by_id(id, retornar_dto)
        if user is None:
            raise ValueError(f"User with id {id} not found")
        return user


        
       