from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from app.users.domain.port.IUserRepository import IUserRepository
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.users.infrastructure.mappers.aggregate_to_model import Aggregate_to_model
from app.users.infrastructure.mappers.model_to_dto import model_to_dto
from app.users.infrastructure.model.ModelUser import User
from app.users.application.dtos.UserDto import UserDto

class UserRepository(IUserRepository[User]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_aggregate: AggregateUser) -> None:
        if self.session is not None:
            user_model = Aggregate_to_model(user_aggregate)
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)
         
    async def IsExistUserName(self, user_name: str) -> UserDto:
        if self.session is not None:
            result = await self.session.exec(select(User).filter_by(username= user_name))
            user = result.scalars().first()
            if user is None:
                return None
            return model_to_dto(user) #retorna el user 
   
    async def IsExistEmail(self, email_user: str) -> UserDto:
        if self.session is not None:
            result = await self.session.exec(select(User).filter_by(email= email_user))
            user = result.scalars().first()
            if user is None:
                return None
            return model_to_dto(user) #retorna el user 

    async def get_users(self) -> List[UserDto]:  
        result = await self.session.exec(select(User))
        user_models = result.scalars().all()
        return [model_to_dto(user_model) for user_model in user_models]
    
    async def update_user(self, user_id: str, user_aggregate: AggregateUser) -> None:
        pass   

    async def delete_user(self, user_id: str) -> None:
        pass

    async def get_user_by_id(self, user_id: str) -> User:
        pass  
    
    async def get_user_me(self) -> None:
        pass

   