from typing import Generic, TypeVar, List, Tuple
from abc import ABC, abstractmethod

T = TypeVar('T')

class IOrderRepository(ABC, Generic[T]):

    @abstractmethod
    async def create_order(self) -> None:
        pass

    @abstractmethod
    async def update_order_state_by_id(self) -> None:
        pass

    @abstractmethod
    async def get_order_by_id(self, order_id: str)-> T:
        pass

    @abstractmethod
    async def get_orders(self, user_id: str) -> List[T]:
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str) -> None:
        pass

    @abstractmethod
    async def create_order_item(self) -> None:
        pass

    @abstractmethod
    async def get_order_items(self, order_id: str) -> List[Tuple[str, int]]:
        pass

    @abstractmethod
    async def get_total_sales(self) -> int:
        pass

    @abstractmethod
    async def get_sales_by_product_id(self, product_id: str) -> T:
        pass

    @abstractmethod
    async def get_total_profit(self) -> T:
        pass

    @abstractmethod
    async def get_profit_by_product_id(self, product_id: str) -> T:
        pass

    @abstractmethod
    async def get_top_selling_products(self, limit: int) -> List[Tuple[str, int]]:
        pass

    @abstractmethod
    async def get_top_customers(self, limit: int) -> List[Tuple[str, int]]:
        pass
    
    