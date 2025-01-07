import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.products.application.services.createProduct import CreateProductService
from app.products.application.services.getProductById import GetProductByIdService
from app.products.application.services.getProducts import GetProductsService
from app.products.application.services.updateProduct import UpdateProductService
from app.products.application.services.deleteProduct import DeleteProductService

from app.products.application.dtos.createProductDto import CreateProductDto
from app.products.application.dtos.updateProductDto import UpdateProductDto
from app.products.domain.aggregate_root import ProductAggregate

# Fixtures
@pytest.fixture
def mock_repo():
    return AsyncMock()

@pytest.fixture
def create_product_service(mock_repo):
    return CreateProductService(repo=mock_repo)

@pytest.fixture
def get_product_by_id_service(mock_repo):
    return GetProductByIdService(repo=mock_repo)

@pytest.fixture
def get_products_service(mock_repo):
    return GetProductsService(repo=mock_repo)

@pytest.fixture
def update_product_service(mock_repo):
    return UpdateProductService(repo=mock_repo)

@pytest.fixture
def delete_product_service(mock_repo):
    return DeleteProductService(repo=mock_repo)

@pytest.fixture
def create_product_dto():
    return CreateProductDto(
        name="Example Product",
        code="EX123",
        description="This is an example product.",
        profit_margin=20.0,
        cost=50.0
    )

@pytest.fixture
def update_product_dto():
    return UpdateProductDto(
        name="Updated Product",
        code="UP123",
        description="This is an updated product.",
        profit_margin=25.0,
        cost=55.0,
        status="active"
    )

@pytest.fixture
def product_aggregate():
    return ProductAggregate.create(
        id=str(uuid4()),
        name="Example Product",
        code="EX123",
        description="This is an example product.",
        margin_profit=20.0,
        cost=50.0,
        status="active"
    )

# CreateProductService
@pytest.mark.asyncio
async def test_create_product_success(create_product_service, create_product_dto, mock_repo):
    mock_repo.get_products.return_value = []

    product_aggregate = await create_product_service.create_product(create_product_dto)

    assert product_aggregate.product.name.get() == create_product_dto.name
    assert product_aggregate.product.code.get() == create_product_dto.code
    assert product_aggregate.product.description.get() == create_product_dto.description
    assert product_aggregate.product.margin_profit.get() == create_product_dto.profit_margin
    assert product_aggregate.product.cost.get() == create_product_dto.cost
    assert product_aggregate.product.status.value == "active"

    mock_repo.create_product.assert_awaited_once_with(product_aggregate)

@pytest.mark.asyncio
async def test_create_product_code_exists(create_product_service, create_product_dto, product_aggregate, mock_repo):
    mock_repo.get_products.return_value = [product_aggregate]

    with pytest.raises(ValueError) as exc_info:
        await create_product_service.create_product(create_product_dto)

    assert str(exc_info.value) == f"Product with code {create_product_dto.code} already exists"

# GetProductByIdService
@pytest.mark.asyncio
async def test_get_product_by_id_success(get_product_by_id_service, product_aggregate, mock_repo):
    mock_repo.get_product_by_id.return_value = product_aggregate

    result = await get_product_by_id_service.get_product_by_id(product_aggregate.product.id)

    assert result == product_aggregate
    mock_repo.get_product_by_id.assert_awaited_once_with(product_aggregate.product.id)

@pytest.mark.asyncio
async def test_get_product_by_id_not_found(get_product_by_id_service, mock_repo):
    mock_repo.get_product_by_id.return_value = None

    product_id = str(uuid4())
    with pytest.raises(ValueError) as exc_info:
        await get_product_by_id_service.get_product_by_id(product_id)

    assert str(exc_info.value) == f"Product with id {product_id} not found"
    mock_repo.get_product_by_id.assert_awaited_once_with(product_id)

# GetProductsService
@pytest.mark.asyncio
async def test_list_products_success(get_products_service, product_aggregate, mock_repo):
    mock_repo.get_products.return_value = [product_aggregate]

    result = await get_products_service.list_products()

    assert result == [product_aggregate]
    mock_repo.get_products.assert_awaited_once()

# UpdateProductService
@pytest.mark.asyncio
async def test_update_product_success(update_product_service, product_aggregate, update_product_dto, mock_repo):
    mock_repo.get_product_by_id.return_value = product_aggregate
    mock_repo.get_products.return_value = [product_aggregate]

    result = await update_product_service.update_product(product_aggregate.product.id, update_product_dto)

    assert result is True
    assert product_aggregate.product.name.get() == update_product_dto.name
    assert product_aggregate.product.code.get() == update_product_dto.code
    assert product_aggregate.product.description.get() == update_product_dto.description
    assert product_aggregate.product.margin_profit.get() == update_product_dto.profit_margin
    assert product_aggregate.product.cost.get() == update_product_dto.cost
    assert product_aggregate.product.status.value == update_product_dto.status

    mock_repo.update_product.assert_awaited_once_with(product_aggregate)

@pytest.mark.asyncio
async def test_update_product_not_found(update_product_service, update_product_dto, mock_repo):
    mock_repo.get_product_by_id.return_value = None

    product_id = str(uuid4())
    with pytest.raises(ValueError) as exc_info:
        await update_product_service.update_product(product_id, update_product_dto)

    assert str(exc_info.value) == f"Product with id {product_id} not found"
    mock_repo.get_product_by_id.assert_awaited_once_with(product_id)
    mock_repo.update_product.assert_not_called()

# DeleteProductService
@pytest.mark.asyncio
async def test_delete_product_success(delete_product_service, product_aggregate, mock_repo):
    mock_repo.get_product_by_id.return_value = product_aggregate

    result = await delete_product_service.delete_product(product_aggregate.product.id)

    assert result is True
    mock_repo.delete_product.assert_awaited_once_with(product_aggregate.product.id)

@pytest.mark.asyncio
async def test_delete_product_not_found(delete_product_service, mock_repo):
    mock_repo.get_product_by_id.return_value = None

    product_id = str(uuid4())
    with pytest.raises(ValueError) as exc_info:
        await delete_product_service.delete_product(product_id)

    assert str(exc_info.value) == f"Product with id {product_id} not found"
    mock_repo.get_product_by_id.assert_awaited_once_with(product_id)
    mock_repo.delete_product.assert_not_called()