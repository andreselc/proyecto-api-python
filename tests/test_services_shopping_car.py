import pytest
from unittest.mock import AsyncMock

from app.shopping_cart.application.services.addShoppinCartProduct import AddShoppinCartProductService
from app.shopping_cart.application.services.deleteShoppinCartProduct import DeleteShoppinCartProductService
from app.shopping_cart.application.services.getShoppinCartProductById import GetShoppinCartProductById
from app.shopping_cart.application.services.getShoppinCartProducts import GetShoppinCartProducts
from app.shopping_cart.application.services.updateShoopinCartProduct import updateShoppinCartProductService

from app.shopping_cart.application.dtos.addShoppingCartDto import AddShoppiCartDto
from app.shopping_cart.application.dtos.updateShoppingCartDto import UpdateInventoryDto
from app.shopping_cart.application.dtos.shoppingCartDto import ShoppinCartDto
from app.shopping_cart.domain.aggregate.aggregate_shoppinCart import ShoppinCartAggregate
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.inventory.domain.aggregate.aggregate_inventory import InventoryAggregate
from app.products.domain.aggregate_root import ProductAggregate

from app.shopping_cart.domain.value_objects.id import ID
# Pruebas unitarias para los servicios de aplicacion de carrito de compra
# -------------------------------------------------------- Servicios de Aplicacion------------------------------------------------------

# Prueba unitaria para el servicio de aplicacion AddShoppinCartProductService
@pytest.fixture
def mock_repo():
    # Mock del repositorio
    repo = AsyncMock()
    return repo

@pytest.fixture
def add_shoppin_cart_service(mock_repo):
    # Servicio con el mock del repositorio
    return AddShoppinCartProductService(repo=mock_repo)

@pytest.fixture
def add_shopping_cart_dto():
    # DTO de carrito de compras con datos de ejemplo
    return AddShoppiCartDto(quantity=3, product_id="product_123")

@pytest.fixture
def product_aggregate():
    # Producto simulado
    product = ProductAggregate.create(
        id="product_123",
        name="Example Product",
        code="EX123",
        description="Example Description",
        margin_profit=20.5,
        cost=50.0,
        status="active"
    )
    return product

@pytest.fixture
def user_aggregate():
    # Usuario simulado
    user = AggregateUser.create(
        id="user_123",
        name="John Doe",
        username="johndoe",
        email="john@example.com",
        password="securepassword",
        role="manager"
    )
    return user

@pytest.fixture
def inventory_aggregate():
    # Inventario simulado
    inventory = InventoryAggregate.create(
        quantity=10,
        product_id="product_123",
        name="Example Product",
        code="EX123",
        description="Example Description",
        margin_profit=20.0,
        cost=50.0,
        status="active"
    )
    return inventory

@pytest.mark.asyncio
async def test_add_shoppin_cart_product_success(
    add_shoppin_cart_service,
    mock_repo,
    add_shopping_cart_dto,
    product_aggregate,
    user_aggregate,
    inventory_aggregate,
):
    # Configurar el mock para no encontrar carritos previos
    mock_repo.get_shoppin_cart_products.return_value = []

    # Llamar al servicio
    result = await add_shoppin_cart_service.add_shoppin_cart_product(
        shoppin_cart_dto=add_shopping_cart_dto,
        product_aggregate=product_aggregate,
        user_aggregate=user_aggregate,
        inventory_aggregate=inventory_aggregate,
    )

    # Verificar que se llamó al método del repositorio para agregar el producto al carrito
    mock_repo.add_shoppin_cart_product.assert_awaited_once()

    # Verificar que el resultado es un agregado de carrito de compras
    assert isinstance(result, ShoppinCartAggregate)
    assert result.shoppin_cart.quantity.get() == add_shopping_cart_dto.quantity



# Prueba unitaria para el servicio de aplicacion DeleteShoppinCartProductService
@pytest.mark.asyncio
async def test_delete_shoppin_cart_product():
    # Crear un mock del repositorio
    mock_repo = AsyncMock()
    
    # Crear una instancia del servicio con el repositorio mockeado
    service = DeleteShoppinCartProductService(repo=mock_repo)
    
    # Definir los parámetros de prueba
    inventory_id = "test_inventory_id"
    user_id = "test_user_id"
    product_id = "test_product_id"
    
    # Configurar el mock para que devuelva un ShoppinCartAggregate cuando se llame a get_shoppin_cart_product_by_id
    mock_repo.get_shoppin_cart_product_by_id.return_value = ShoppinCartAggregate.create(
        id="1234",
        quantity=1,
        product_id="test_product_id",
        name="product_name",
        code="product_code",
        description="product_description",
        margin_profit=10.0,
        cost=100.0,
        status="active",
        user_id="test_user_id",
        user_name="user_name",
        username="username",
        email="user@example.com",
        password="password",
        role="manager",
        inventory_quantity=10
    )    
    # Llamar al método del servicio
    result = await service.delete_shoppin_cart_product(inventory_id, user_id, product_id)
    
    # Verificar que el método del repositorio fue llamado con los parámetros correctos
    mock_repo.get_shoppin_cart_product_by_id.assert_called_once_with(inventory_id, user_id, product_id)
    mock_repo.delete_shoppin_cart_product.assert_called_once_with(inventory_id, user_id)
    
    # Verificar que el resultado es True
    assert result is True

@pytest.mark.asyncio
async def test_delete_shoppin_cart_product_not_found():
    # Crear un mock del repositorio
    mock_repo = AsyncMock()
    
    # Crear una instancia del servicio con el repositorio mockeado
    service = DeleteShoppinCartProductService(repo=mock_repo)
    
    # Definir los parámetros de prueba
    inventory_id = "test_inventory_id"
    user_id = "test_user_id"
    product_id = "test_product_id"
    
    # Configurar el mock para que devuelva None cuando se llame a get_shoppin_cart_product_by_id
    mock_repo.get_shoppin_cart_product_by_id.return_value = None
    
    # Verificar que se lanza una excepción cuando el producto no se encuentra
    with pytest.raises(ValueError, match=f"Product with inventory id {inventory_id} not added"):
        await service.delete_shoppin_cart_product(inventory_id, user_id, product_id)
    
    # Verificar que delete_shoppin_cart_product no fue llamado
    mock_repo.delete_shoppin_cart_product.assert_not_called()



# Prueba unitaria para el servicio de aplicacion GetShoppinCartProductById
@pytest.fixture
def get_shoppin_cart_service(mock_repo):
    # Servicio con el mock del repositorio
    return GetShoppinCartProductById(repo=mock_repo)

@pytest.fixture
def shopping_cart_aggregate():
    # Agregado de carrito de compras simulado
    return ShoppinCartAggregate.create(
        id="cart_123",
        quantity=3,
        product_id="product_123",
        name="Example Product",
        code="EX123",
        description="Example Description",
        margin_profit=20.5,
        cost=50.0,
        status="active",
        user_id="user_123",
        user_name="John Doe",
        username="johndoe",
        email="john@example.com",
        password="securepassword",
        role="manager",
        inventory_quantity=10
    )

@pytest.mark.asyncio
async def test_get_shoppin_cart_product_by_id_success(
    get_shoppin_cart_service,
    mock_repo,
    shopping_cart_aggregate,
):
    # Configurar el mock para devolver un agregado válido
    mock_repo.get_shoppin_cart_product_by_id.return_value = shopping_cart_aggregate

    # Llamar al servicio
    result = await get_shoppin_cart_service.get_shoppin_cart_product_by_id(
        inventory_id="inventory_123",
        user_id="user_123",
        product_id="product_123"
    )

    # Verificar que el resultado es el esperado
    assert result == shopping_cart_aggregate
    mock_repo.get_shoppin_cart_product_by_id.assert_awaited_once_with("inventory_123", "user_123", "product_123")

@pytest.mark.asyncio
async def test_get_shoppin_cart_product_by_id_not_found(get_shoppin_cart_service, mock_repo):
    # Configurar el mock para devolver None
    mock_repo.get_shoppin_cart_product_by_id.return_value = None

    # Verificar que se lanza una excepción cuando no se encuentra el producto
    with pytest.raises(ValueError) as exc:
        await get_shoppin_cart_service.get_shoppin_cart_product_by_id(
            inventory_id="inventory_123",
            user_id="user_123",
            product_id="product_456"
        )

    # Asegurar que el mensaje de error es el esperado
    assert str(exc.value) == "Product with inventory id inventory_123 not added to shopping cart"
    mock_repo.get_shoppin_cart_product_by_id.assert_awaited_once_with("inventory_123", "user_123", "product_456")



# Prueba unitaria para el servicio de aplicacion GetShoppinCartProducts
@pytest.fixture
def get_shoppin_cart_products_service(mock_repo):
    # Servicio con el mock del repositorio
    return GetShoppinCartProducts(repo=mock_repo)

@pytest.fixture
def shopping_cart_aggregates():
    # Lista simulada de agregados de carrito de compras
    return [
        ShoppinCartAggregate.create(
            id="cart_123",
            quantity=3,
            product_id="product_123",
            name="Example Product",
            code="EX123",
            description="Example Description",
            margin_profit=20.5,
            cost=50.0,
            status="active",
            user_id="user_123",
            user_name="John Doe",
            username="johndoe",
            email="john@example.com",
            password="securepassword",
            role="manager",
            inventory_quantity=10
        ),
        ShoppinCartAggregate.create(
            id="cart_124",
            quantity=1,
            product_id="product_124",
            name="Another Product",
            code="EX124",
            description="Another Description",
            margin_profit=15.0,
            cost=30.0,
            status="active",
            user_id="user_123",
            user_name="John Doe",
            username="johndoe",
            email="john@example.com",
            password="securepassword",
            role="manager",
            inventory_quantity=5
        ),
    ]

@pytest.mark.asyncio
async def test_get_shoppin_cart_products_success(
    get_shoppin_cart_products_service,
    mock_repo,
    shopping_cart_aggregates,
):
    # Configurar el mock para devolver una lista de agregados
    mock_repo.get_shoppin_cart_products.return_value = shopping_cart_aggregates

    # Llamar al servicio
    result = await get_shoppin_cart_products_service.get_shoppin_cart_products(user_id="user_123")

    # Verificar que el resultado es el esperado
    assert result == shopping_cart_aggregates
    mock_repo.get_shoppin_cart_products.assert_awaited_once_with("user_123")



# Prueba unitaria para el servicio de aplicacion updateShoopinCartProductService
@pytest.fixture
def update_shoppin_cart_product_service(mock_repo):
    # Servicio con el mock del repositorio
    return updateShoppinCartProductService(repo=mock_repo)

@pytest.fixture
def update_shopping_cart_dto():
    # DTO para la actualización del carrito de compras
    return UpdateInventoryDto(quantity=5)

@pytest.fixture
def shopping_cart_aggregate():
    # Agregado simulado de carrito de compras
    return ShoppinCartAggregate.create(
        id="cart_123",
        quantity=3,
        product_id="product_123",
        name="Example Product",
        code="EX123",
        description="Example Description",
        margin_profit=20.5,
        cost=50.0,
        status="active",
        user_id="user_123",
        user_name="John Doe",
        username="johndoe",
        email="john@example.com",
        password="securepassword",
        role="manager",
        inventory_quantity=10
    )

@pytest.fixture
def inventory_aggregate():
    # Inventario simulado
    inventory = InventoryAggregate.create(
        quantity=10,
        product_id="product_123",
        name="Example Product",
        code="EX123",
        description="Example Description",
        margin_profit=20.0,
        cost=50.0,
        status="active"
    )
    return inventory

@pytest.mark.asyncio
async def test_update_shoppin_cart_product_success(
    update_shoppin_cart_product_service,
    mock_repo,
    update_shopping_cart_dto,
    shopping_cart_aggregate,
    inventory_aggregate,
):
    # Configurar el mock para devolver el agregado correspondiente
    mock_repo.get_shoppin_cart_product_by_id.return_value = shopping_cart_aggregate

    # Llamar al servicio
    result = await update_shoppin_cart_product_service.update_shoppin_cart_product(
        inventory_aggregate=inventory_aggregate,
        user_id="user_123",
        product_id="product_123",
        shoppin_cart_dto=update_shopping_cart_dto
    )

    # Verificar que el método del repositorio para obtener el producto fue llamado
    mock_repo.get_shoppin_cart_product_by_id.assert_awaited_once_with(inventory_aggregate.inventory.id.get(), "user_123", "product_123")

    # Verificar que el método del repositorio para actualizar el producto fue llamado
    mock_repo.update_shoppin_cart_product.assert_awaited_once_with(shopping_cart_aggregate, inventory_aggregate.inventory.id.get())

    # Verificar que el resultado sea True
    assert result is True
    assert shopping_cart_aggregate.shoppin_cart.quantity.get() == update_shopping_cart_dto.quantity

@pytest.mark.asyncio
async def test_update_shoppin_cart_product_not_found(
    update_shoppin_cart_product_service,
    mock_repo,
    update_shopping_cart_dto,
    inventory_aggregate,
):
    # Configurar el mock para que no se encuentre el producto
    mock_repo.get_shoppin_cart_product_by_id.return_value = None

    # Verificar que se lanza una excepción al intentar actualizar un producto inexistente
    with pytest.raises(ValueError) as exc:
        await update_shoppin_cart_product_service.update_shoppin_cart_product(
            inventory_aggregate=inventory_aggregate,
            user_id="user_123",
            product_id="product_456",
            shoppin_cart_dto=update_shopping_cart_dto
        )

    # Asegurar que el mensaje de error es el esperado
    assert str(exc.value) == "No product associated with that id product_456 in the shopping cart"
    mock_repo.get_shoppin_cart_product_by_id.assert_awaited_once_with(inventory_aggregate.inventory.id.get(), "user_123", "product_456")

