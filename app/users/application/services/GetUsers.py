from app.users.domain.port.IUserRepository import IUserRepository 
from app.users.application.dtos.UserDto import UserDto
from app.users.domain.aggregate.aggregate_user import AggregateUser

class GetUsers:
    def __init__(self, repo: IUserRepository[AggregateUser]):
        self.repo = repo

    async def list_users(self, role:str) -> list[UserDto]:
        users = await self.repo.get_users(role)
        return users