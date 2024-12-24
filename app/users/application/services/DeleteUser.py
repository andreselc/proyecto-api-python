from app.users.domain.port.IUserRepository import IUserRepository 
from app.users.domain.aggregate.aggregate_user import AggregateUser
from fastapi import HTTPException, status


class DeleteUser:
    def __init__(self, repo: IUserRepository[AggregateUser]):
        self.repo = repo

    async def delete_user_id(self, id: str) -> bool:
        user = await self.repo.IsExistUserName("superadmin")
        if (user.id == id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can't delete the superadmin user"
            )

        await self.repo.delete_user(id)
        return True