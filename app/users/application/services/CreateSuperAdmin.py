from app.users.domain.port.IUserRepository import IUserRepository 
from app.users.domain.aggregate.aggregate_user import AggregateUser


class CreateSuperAdmin:
    def __init__(self, repo: IUserRepository[AggregateUser]):
        self.repo = repo

    async def create_super_admin(self) -> bool:
        existing_user = await self.repo.IsExistUserName("superadmin")
        
        if(existing_user is not None):
            return False
        
        user = AggregateUser.create(
            name = "Daniel",
            email= "ecommerce_superadmin@gmail.com",
            username= "superadmin",
            password= "ContraSupAdmin123",
            role= "superadmin"
        )
        
        await self.repo.create_user(user)
        return True
     
    