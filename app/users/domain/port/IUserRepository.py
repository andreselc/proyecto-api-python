from typing import Generic, TypeVar, List
from abc import ABC, abstractmethod

T = TypeVar('T')

class IUserRepository(ABC, Generic[T]):
    
    @abstractmethod
    async def create_user(self) -> None:
        pass

    @abstractmethod
    async def update_user(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def delete_user(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> T:
        pass

    @abstractmethod
    async def get_users(self, user_role: str) -> List[T]:
        pass

    @abstractmethod
    async def get_user_me(self) -> None:
        pass

    @abstractmethod
    async def IsExistSuperAdmin(self) -> None:
        pass
