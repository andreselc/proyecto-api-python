import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.inventory.application.services.createInventory import CreateInventoryService
from app.inventory.application.services.getInventoryById import GetInventoryByIdService
from app.inventory.application.services.getInventoryByProductId import GetInventoryByProductIdService
from app.inventory.application.services.updateInventory import UpdateInventoryService
from app.products.domain.aggregate_root import ProductAggregate

from app.inventory.application.dtos.createInventoryDto import CreateInventoryDto
from app.inventory.application.dtos.updateInventoryDto import UpdateInventoryDto
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate

# Fixtures
@pytest.fixture
def mock_repo():
    return AsyncMock()

@pytest.fixture
def create_inventory_service(mock_repo):
    return CreateInventoryService(repo=mock_repo)

@pytest.fixture
def inventory_dto():
    return CreateInventoryDto(quantity=10, product_id="product_123")

@pytest.fixture
def product_aggregate():
    product_name = "Example Product"
    product_code = "EX123"
    product_description = "This is an example product."
    product_margin_profit = 20.0
    product_cost = 50.0

    product_aggregate = ProductAggregate.create("product_123", product_name, product_code, product_description, product_margin_profit, product_cost, "active")
    return product_aggregate

@pytest.mark.asyncio
async def test_create_inventory_success(create_inventory_service, inventory_dto, product_aggregate, mock_repo):
    mock_repo.create_inventory = AsyncMock()

    inventory_aggregate = await create_inventory_service.create_inventory(inventory_dto, product_aggregate)

    assert inventory_aggregate.inventory.quantity.get() == inventory_dto.quantity
    assert inventory_aggregate.product.name.get() == product_aggregate.product.name.get()
    assert inventory_aggregate.product.code.get() == product_aggregate.product.code.get()
    assert inventory_aggregate.product.description.get() == product_aggregate.product.description.get()
    assert inventory_aggregate.product.margin_profit.get() == product_aggregate.product.margin_profit.get()
    assert inventory_aggregate.product.cost.get() == product_aggregate.product.cost.get()
    assert inventory_aggregate.product.status.value == "active"

    mock_repo.create_inventory.assert_awaited_once_with(inventory_aggregate)

@pytest.mark.asyncio
async def test_create_inventory_repository_error(create_inventory_service, inventory_dto, product_aggregate, mock_repo):
    mock_repo.create_inventory.side_effect = Exception("Repository error")
    
    with pytest.raises(Exception) as exc_info:
        await create_inventory_service.create_inventory(inventory_dto, product_aggregate)
    
    assert str(exc_info.value) == "Repository error"
    mock_repo.create_inventory.assert_awaited_once()

# Tests for GetInventoryByIdService
@pytest.fixture
def get_inventory_by_id_service(mock_repo):
    return GetInventoryByIdService(repo=mock_repo)

@pytest.fixture
def inventory_aggregate():
    return InventoryAggregate.create(
        quantity=10,
        product_id="product_123",
        name="Example Product",
        code="EX123",
        description="This is an example product.",
        margin_profit=20.0,
        cost=50.0,
        status="active"
    )

@pytest.mark.asyncio
async def test_get_inventory_by_id_success(get_inventory_by_id_service, mock_repo, inventory_aggregate):
    mock_repo.get_inventory_by_id.return_value = inventory_aggregate

    inventory_id = "inventory_123"
    result = await get_inventory_by_id_service.get_inventory_by_id(inventory_id)

    assert result == inventory_aggregate
    mock_repo.get_inventory_by_id.assert_awaited_once_with(inventory_id)

@pytest.mark.asyncio
async def test_get_inventory_by_id_not_found(get_inventory_by_id_service, mock_repo):
    mock_repo.get_inventory_by_id.return_value = None

    inventory_id = "nonexistent_id"
    with pytest.raises(ValueError) as exc_info:
        await get_inventory_by_id_service.get_inventory_by_id(inventory_id)

    assert str(exc_info.value) == f"Inventory with id {inventory_id} not found"
    mock_repo.get_inventory_by_id.assert_awaited_once_with(inventory_id)

# Tests for UpdateInventoryService
@pytest.fixture
def update_inventory_service(mock_repo):
    return UpdateInventoryService(repo=mock_repo)

@pytest.fixture
def update_inventory_dto():
    return UpdateInventoryDto(quantity=15)

@pytest.mark.asyncio
async def test_update_inventory_success(update_inventory_service, mock_repo, inventory_aggregate, update_inventory_dto):
    mock_repo.get_inventory_by_id.return_value = inventory_aggregate
    mock_repo.update_inventory = AsyncMock()

    inventory_id = "inventory_123"
    result = await update_inventory_service.update_inventory(inventory_id, update_inventory_dto)

    assert result is True
    assert inventory_aggregate.inventory.quantity.get() == update_inventory_dto.quantity

    mock_repo.get_inventory_by_id.assert_awaited_once_with(inventory_id)
    mock_repo.update_inventory.assert_awaited_once_with(inventory_aggregate)

@pytest.mark.asyncio
async def test_update_inventory_not_found(update_inventory_service, mock_repo, update_inventory_dto):
    mock_repo.get_inventory_by_id.return_value = None

    inventory_id = "nonexistent_id"
    with pytest.raises(ValueError) as exc_info:
        await update_inventory_service.update_inventory(inventory_id, update_inventory_dto)

    assert str(exc_info.value) == f"Inventory with id {inventory_id} not found"
    mock_repo.get_inventory_by_id.assert_awaited_once_with(inventory_id)
    mock_repo.update_inventory.assert_not_called()

# Tests for GetInventoryByProductIdService
@pytest.fixture
def get_inventory_by_product_id_service(mock_repo):
    return GetInventoryByProductIdService(repo=mock_repo)

@pytest.mark.asyncio
async def test_get_inventory_by_product_id_success(get_inventory_by_product_id_service, mock_repo, inventory_aggregate):
    mock_repo.get_inventory_by_product_id.return_value = inventory_aggregate

    product_id = "product_123"
    result = await get_inventory_by_product_id_service.get_inventory_by_product_id(product_id)

    assert result == inventory_aggregate
    mock_repo.get_inventory_by_product_id.assert_awaited_once_with(product_id)

@pytest.mark.asyncio
async def test_get_inventory_by_product_id_not_found(get_inventory_by_product_id_service, mock_repo):
    mock_repo.get_inventory_by_product_id.return_value = None

    product_id = "nonexistent_product_id"
    with pytest.raises(ValueError) as exc_info:
        await get_inventory_by_product_id_service.get_inventory_by_product_id(product_id)

    assert str(exc_info.value) == f"There is no product with that id {product_id} associated with an inventory "
    mock_repo.get_inventory_by_product_id.assert_awaited_once_with(product_id)