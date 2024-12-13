from app.users.domain.port import IUserRepository
from app.users.infrastructure.model.ModelUser import User
from sqlmodel.ext.asyncio.session import AsyncSession
from app.users.infrastructure.db.database import get_session


class UserRepository(IUserRepository[User]):
    def __init__(self, session: AsyncSession = get_session()):
        self.db = session

    async def create_user(self, user: User):
        await self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)