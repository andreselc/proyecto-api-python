from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from app.users.domain.port.IUserRepository import IUserRepository
from app.users.infrastructure.model.ModelUser import User
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.users.infrastructure.mappers.aggregate_to_model import Aggregate_to_model

class UserRepository(IUserRepository[User]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_aggregate: AggregateUser) -> None:
        if self.session is not None:
            user_model = Aggregate_to_model(user_aggregate)
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)
    
    async def IsExistSuperAdmin(self) -> None | bool:
        if self.session is not None:
            result = await self.session.exec(select(User).filter_by(role='superadmin'))
            return result.scalars().first() is None #retorna true si no existe un superadmin en la base de datos
      
           
    async def update_user(self, user_id: str, user_aggregate: AggregateUser) -> None:
        pass   

    async def delete_user(self, user_id: str) -> None:
        pass

    async def get_user_by_id(self, user_id: str) -> User:
        pass  
    
    async def get_users(self, user_role: str) -> List[User]:
        pass
    
    async def get_user_me(self) -> None:
        pass

   