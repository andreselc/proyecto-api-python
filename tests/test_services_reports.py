import pytest
from unittest.mock import AsyncMock
from app.orders.application.services.getTotalSales import GetTotalSalesService
from app.orders.application.services.getTotalProfit import GetTotalProfitService
from app.orders.application.services.getSalesByProductId import GetSalesByProductIdService
from app.orders.application.services.getProfitByProductId import GetProfitByProductIdService
from app.orders.application.services.getTopSellingProductsService import GetTopSellingProductsService
from app.orders.application.services.getTopCustomersService import GetTopCustomersService
from app.orders.domain.aggregate.aggregate_order import OrderAggregate
from app.orders.domain.ports.IOrderRepository import IOrderRepository

# Fixtures
@pytest.fixture
def mock_repo():
    return AsyncMock(spec=IOrderRepository)

@pytest.fixture
def get_total_sales_service(mock_repo):
    return GetTotalSalesService(repo=mock_repo)

@pytest.fixture
def get_total_profit_service(mock_repo):
    return GetTotalProfitService(repo=mock_repo)

@pytest.fixture
def get_sales_by_product_id_service(mock_repo):
    return GetSalesByProductIdService(repo=mock_repo)

@pytest.fixture
def get_profit_by_product_id_service(mock_repo):
    return GetProfitByProductIdService(repo=mock_repo)

@pytest.fixture
def get_top_selling_products_service(mock_repo):
    return GetTopSellingProductsService(repo=mock_repo)

@pytest.fixture
def get_top_customers_service(mock_repo):
    return GetTopCustomersService(repo=mock_repo)

# Tests for GetTotalSalesService
@pytest.mark.asyncio
async def test_get_total_sales_success(get_total_sales_service, mock_repo):
    mock_repo.get_total_sales.return_value = 1000

    result = await get_total_sales_service.get_total_sales()

    assert result == 1000
    mock_repo.get_total_sales.assert_awaited_once()

# Tests for GetTotalProfitService
@pytest.mark.asyncio
async def test_get_total_profit_success(get_total_profit_service, mock_repo):
    mock_repo.get_total_profit.return_value = 5000.0

    result = await get_total_profit_service.get_total_profit()

    assert result == 5000.0
    mock_repo.get_total_profit.assert_awaited_once()

# Tests for GetSalesByProductIdService
@pytest.mark.asyncio
async def test_get_sales_by_product_id_success(get_sales_by_product_id_service, mock_repo):
    product_id = "product123"
    mock_repo.get_sales_by_product_id.return_value = 200

    result = await get_sales_by_product_id_service.get_sales_by_product_id(product_id)

    assert result == 200
    mock_repo.get_sales_by_product_id.assert_awaited_once_with(product_id)

# Tests for GetProfitByProductIdService
@pytest.mark.asyncio
async def test_get_profit_by_product_id_success(get_profit_by_product_id_service, mock_repo):
    product_id = "product123"
    mock_repo.get_profit_by_product_id.return_value = 1500.0

    result = await get_profit_by_product_id_service.get_profit_by_product_id(product_id)

    assert result == 1500.0
    mock_repo.get_profit_by_product_id.assert_awaited_once_with(product_id)

# Tests for GetTopSellingProductsService
@pytest.mark.asyncio
async def test_get_top_selling_products_success(get_top_selling_products_service, mock_repo):
    limit = 5
    top_selling_products = [("product1", 100), ("product2", 90)]
    mock_repo.get_top_selling_products.return_value = top_selling_products

    result = await get_top_selling_products_service.get_top_selling_products(limit)

    assert result == top_selling_products
    mock_repo.get_top_selling_products.assert_awaited_once_with(limit)

# Tests for GetTopCustomersService
@pytest.mark.asyncio
async def test_get_top_customers_success(get_top_customers_service, mock_repo):
    limit = 5
    top_customers = [("customer1", 1000), ("customer2", 900)]
    mock_repo.get_top_customers.return_value = top_customers

    result = await get_top_customers_service.get_top_customers(limit)

    assert result == top_customers
    mock_repo.get_top_customers.assert_awaited_once_with(limit)