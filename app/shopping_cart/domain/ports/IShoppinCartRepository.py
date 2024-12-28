from typing import Generic, TypeVar, List
from abc import ABC, abstractmethod

T = TypeVar('T')

class IShoppinCartRepository(ABC, Generic[T]):

    @abstractmethod
    async def add_shoppin_cart_product(self) -> None:
        pass

    @abstractmethod
    async def update_shoppin_cart_product(self) -> None:
        pass

    @abstractmethod
    async def delete_shoppin_cart_product(self, shoppin_cart_id: str) -> None:
        pass

    @abstractmethod
    async def get_shoppin_cart_products(self, shoppin_cart_id: str, user_id: str) -> List[T]:
        pass

    @abstractmethod
    async def get_shoppin_cart_product_by_id(self, shoppin_cart_id: str) -> T:
        pass