from typing import Generic, TypeVar, List
from abc import ABC, abstractmethod

T = TypeVar('T')

class IInventoryRepository(ABC, Generic[T]):

    @abstractmethod
    async def create_inventory(self) -> None:
        pass

    @abstractmethod
    async def update_inventory(self) -> None:
        pass

    @abstractmethod
    async def get_inventory_by_id(self, inventory_id: str) -> T:
        pass
    
    @abstractmethod
    async def get_inventory_by_product_id(self, product_id: str) -> T:
        pass