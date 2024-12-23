
from app.users.domain.port.IUserRepository import IUserRepository 
from app.users.application.dtos.UpdateUserDto import UpdateUserDto
from app.users.domain.aggregate.aggregate_user import AggregateUser
from fastapi import HTTPException, status

class UpdateUser:
    def __init__(self, repo: IUserRepository[AggregateUser]):
        self.repo = repo

    async def update_user(self, user_id: str, user_dto: UpdateUserDto) -> bool:
        username = await self.repo.IsExistUserName(user_dto.username)
        email = await self.repo.IsExistEmail(user_dto.email)
        user_aggregate = await self.repo.get_user_by_id(user_id, False)
        
        if user_aggregate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        if(user_aggregate.user.role.value == "superadmin"):
            raise ValueError(f"You can't update a superadmin user")
        
        if username is not None:
            raise ValueError(f"The username {user_dto.username} is already registered")

        if email is not None:
            raise ValueError(f"The email {user_dto.email} is already registered")

        
        user_aggregate.update(
            email= user_dto.email,
            username= user_dto.username,
            password= user_dto.password,
            name= user_dto.name
        )
        await self.repo.update_user(user_aggregate)
        return True

      
    