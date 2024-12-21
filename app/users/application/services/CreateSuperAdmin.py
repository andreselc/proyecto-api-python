from app.users.domain.port.IUserRepository import IUserRepository 
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.users.seguridad.auth import get_password_hash

class CreateSuperAdmin:
    def __init__(self, repo: IUserRepository[AggregateUser]):
        self.repo = repo

    async def create_super_admin(self) -> bool:
        existing_user = await self.repo.IsExistSuperAdmin()
        
        if(existing_user is not True):
            return False
        
        user = AggregateUser.create(
            name = "Daniel",
            email= "ecommerce_superadmin@gmail.com",
            username= "superadmin",
            password= get_password_hash("ContraSupAdmin123"),
            role= "superadmin"
        )
        
        await self.repo.create_user(user)
        return True
     
    