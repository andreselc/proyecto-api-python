from typing import Generic, TypeVar, List
from abc import ABC, abstractmethod

T = TypeVar('T')

class IProductRepository(ABC, Generic[T]):
    
    @abstractmethod
    async def create_product(self) -> None:
        pass

    @abstractmethod
    async def update_product(self) -> None:
        pass

    @abstractmethod
    async def delete_product(self, product_id: str) -> None:
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: str) -> T:
        pass

    @abstractmethod
    async def get_products(self) -> List[T]:
        pass