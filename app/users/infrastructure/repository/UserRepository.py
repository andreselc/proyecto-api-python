from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy.future import select
from app.users.domain.port.IUserRepository import IUserRepository
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.users.infrastructure.mappers.aggregate_to_model import Aggregate_to_model
from app.users.infrastructure.mappers.model_to_dto import model_to_dto
from app.users.infrastructure.mappers.model_to_domain import model_to_Aggregate
from app.common.infrastructure.Modelo import User
from app.users.application.dtos.UserDto import UserDto
from fastapi import HTTPException, status

class UserRepository(IUserRepository[User]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_aggregate: AggregateUser) -> None:
        if self.session is not None:
            user_model = Aggregate_to_model(user_aggregate)
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)
         
    async def IsExistUserName(self, user_name: str) -> User:
        if self.session is not None:
            result = await self.session.exec(select(User).where(User.username == user_name))
            user = result.scalars().first()
            if user is None:
                return None
            return user #retorna el user 
   
    async def IsExistEmail(self, email_user: str) -> AggregateUser:
        if self.session is not None:
            result = await self.session.exec(select(User).where(User.email == email_user))
            user = result.scalars().first()
            if user is None:
                return None
            return model_to_dto(user) #retorna el user 

    async def get_users(self, role: str) -> List[UserDto]:  
        if self.session is not None:
            query = select(User)
            if role:
                query = query.where(User.role == role.lower())
            results = await self.session.exec(query)
            user_models = results.scalars().all()
            return [model_to_dto(user_model) for user_model in user_models]
    
    async def update_user(self, user_aggregate: AggregateUser) -> None:
        if self.session is not None:
            user_model= Aggregate_to_model(user_aggregate)
            user_model.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await self.session.merge(user_model)
            await self.session.commit()


    async def delete_user(self, user_id: str) -> None:
        if self.session is not None:
            result = await self.session.exec(select(User).where(User.id == user_id))
            user = result.scalars().first()
            if(user is None):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id {user_id} not found "
                )
            await self.session.delete(user)
            await self.session.commit()


    async def get_user_by_id(self, user_id: str, retorar_dto: bool) -> AggregateUser | UserDto:
        if self.session is not None:
            result = await self.session.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()
            if user is None:
                return None
            if retorar_dto:
                return model_to_dto(user)
            else:
                return model_to_Aggregate(user) 
    


   