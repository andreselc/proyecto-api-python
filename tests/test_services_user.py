from datetime import timedelta, datetime
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException, status
import jwt

from app.users.application.services.UpdateUser import UpdateUser
from app.users.application.services.GetUsers import GetUsers
from app.users.application.services.DeleteUser import DeleteUser
from app.users.application.services.CreateUser import CreateUser
from app.users.application.services.GetUserById import GetUserById
from app.users.application.services.LoginUser import LoginUser

from app.users.auth.auth import SECRET_KEY, ALGORITHM
from app.users.auth.utils import get_password_hash
from app.common.infrastructure.Modelo import User

from app.users.application.dtos.UserDto import UserDto
from app.users.application.dtos.UpdateUserDto import UpdateUserDto  
from app.users.application.dtos.CreateUserDto import CreateUserDto
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.users.application.dtos.LoginUserDto import LoginUserDto
from app.users.application.dtos.LoginRespuestaUserDto import LoginRespuestaUserDto

from uuid import uuid4


#prueba ruta
def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

#pruebas unitarias
# -------------------------------------------------------- Servicios de Aplicacion------------------------------------------------------
@pytest.mark.asyncio
async def test_create_user_success(user_payload):
    # Crear un mock del repositorio
    mock_repo = AsyncMock()
    mock_repo.IsExistUserName.return_value = None  # Simular que el nombre de usuario no existe
    mock_repo.IsExistEmail.return_value = None  # Simular que el correo electrónico no existe
    mock_repo.create_user.return_value = None  # Simular la creación del usuario

    # Crear una instancia del servicio con el mock del repositorio
    service = CreateUser(mock_repo)

    # Crear un DTO de usuario a partir de user_payload
    user_dto = CreateUserDto(**user_payload)

    # Ejecutar el método para crear el usuario
    result = await service.create_user(user_dto)

    # Verificar que el resultado es True (usuario creado)
    assert result is True

    # Verificar que se llamó a IsExistUserName con "johndoe"
    mock_repo.IsExistUserName.assert_called_once_with("johndoe")

    # Verificar que se llamó a IsExistEmail con "john.doe@example.com"
    mock_repo.IsExistEmail.assert_called_once_with("john.doe@example.com")

@pytest.mark.asyncio
async def test_delete_user_success():
    # Crear un mock del repositorio
    mock_repo = AsyncMock()
    user_id = str(uuid4())
    mock_repo.IsExistUserName.return_value = AggregateUser(id=str(uuid4()), user=None)  # Simular que el superadmin existe
    mock_repo.delete_user.return_value = None  # Simular la eliminación del usuario

    # Crear una instancia del servicio con el mock del repositorio
    service = DeleteUser(mock_repo)

    # Ejecutar el método para eliminar el usuario
    result = await service.delete_user_id(user_id)

    # Verificar que el resultado es True (usuario eliminado)
    assert result is True

    # Verificar que se llamó a delete_user con "user_id"
    mock_repo.delete_user.assert_called_once_with(user_id)

@pytest.mark.asyncio
async def test_not_delete_superadmin_user():
    # Crear un mock del repositorio
    mock_repo = AsyncMock()
    superadmin_id = str(uuid4())
    mock_repo.IsExistUserName.return_value = AggregateUser(id=superadmin_id, user=None)  # Simular que el superadmin existe

    # Crear una instancia del servicio con el mock del repositorio
    service = DeleteUser(mock_repo)

    # Ejecutar el método para eliminar el superadmin y verificar que lanza una excepción
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_user_id(superadmin_id)

    # Verificar que la excepción tiene el código de estado correcto y el mensaje de error
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "You can't delete the superadmin user"

    # Verificar que no se llamó a delete_user
    mock_repo.delete_user.assert_not_called()

@pytest.mark.asyncio
async def test_create_user_username_exists(user_payload):
    # Crear un mock del repositorio
    mock_repo = AsyncMock()
    mock_repo.IsExistUserName.return_value = AggregateUser(id=str(uuid4()), user=None)  # Simular que el nombre de usuario ya existe
    mock_repo.IsExistEmail.return_value = None  # Simular que el correo electrónico no existe

    # Crear una instancia del servicio con el mock del repositorio
    service = CreateUser(mock_repo)

    # Crear un DTO de usuario a partir de user_payload
    user_dto = CreateUserDto(**user_payload)

    # Ejecutar el método para crear el usuario y verificar que lanza una excepción
    with pytest.raises(ValueError, match=f"The username {user_dto.username} is already registered"):
        await service.create_user(user_dto)

@pytest.mark.asyncio
async def test_create_user_email_exists(user_payload):
    # Crear un mock del repositorio
    mock_repo = AsyncMock()
    mock_repo.IsExistUserName.return_value = None  # Simular que el nombre de usuario no existe
    mock_repo.IsExistEmail.return_value = AggregateUser(id=str(uuid4()), user=None)  # Simular que el correo electrónico ya existe

    # Crear una instancia del servicio con el mock del repositorio
    service = CreateUser(mock_repo)

    # Crear un DTO de usuario a partir de user_payload
    user_dto = CreateUserDto(**user_payload)

    # Ejecutar el método para crear el usuario y verificar que lanza una excepción
    with pytest.raises(ValueError, match=f"The email {user_dto.email} is already registered"):
        await service.create_user(user_dto)

@pytest.mark.asyncio
async def test_not_create_user_superadmin(user_payload):
    # Crear un mock del repositorio
    mock_repo = AsyncMock()
    mock_repo.IsExistUserName.return_value = None  # Simular que el nombre de usuario no existe
    mock_repo.IsExistEmail.return_value = None  # Simular que el correo electrónico no existe

    # Crear una instancia del servicio con el mock del repositorio
    service = CreateUser(mock_repo)

    # Modificar el payload para que el rol sea "superadmin"
    user_payload["role"] = "superadmin"
    user_dto = CreateUserDto(**user_payload)

    # Ejecutar el método para crear el usuario y verificar que lanza una excepción
    with pytest.raises(ValueError, match="You can't create a superadmin user"):
        await service.create_user(user_dto)    

@pytest.mark.asyncio
async def test_get_user_by_id_success(user_get):
    
    user = UserDto(**user_get)

    # Crear mocks
    mock_repo = AsyncMock()
    mock_repo.get_user_by_id.return_value = user  # Simular la obtención del usuario por ID

    # Crear una instancia del servicio con el mock del repositorio
    service = GetUserById(mock_repo)

    # Ejecutar el método para obtener el usuario por ID
    result = await service.get_user_by_id(user_get["id"], True)

    # Verificar que el resultado es un UserDto
    assert isinstance(result, UserDto)
    assert result.id == user_get["id"]
    assert result.username == user_get["username"]
    assert result.email == user_get["email"]
    assert result.role == user_get["role"]

    # Verificar que se llamó a get_user_by_id con el ID correcto
    mock_repo.get_user_by_id.assert_called_once_with(user_get["id"], True)

@pytest.mark.asyncio
async def test_get_user_by_id_not_found():
    # Crear mocks
    mock_repo = AsyncMock()
    mock_repo.get_user_by_id.return_value = None  # Simular que el usuario no se encuentra

    # Crear una instancia del servicio con el mock del repositorio
    service = GetUserById(mock_repo)

    # Ejecutar el método para obtener el usuario por ID y verificar que lanza una excepción
    user_id = str(uuid4())
    with pytest.raises(ValueError, match=f"User with id {user_id} not found"):
        await service.get_user_by_id(user_id, True)

    # Verificar que se llamó a get_user_by_id con el ID correcto
    mock_repo.get_user_by_id.assert_called_once_with(user_id, True)


@pytest.mark.asyncio
async def test_list_users_success(user_get):
    user = UserDto(**user_get)
    users_list = [user]

    # Crear mocks
    mock_repo = AsyncMock()
    mock_repo.get_users.return_value = users_list  # Simular la obtención de la lista de usuarios

    # Crear una instancia del servicio con el mock del repositorio
    service = GetUsers(mock_repo)

    # Ejecutar el método para listar los usuarios
    result = await service.list_users(user_get["role"])

    # Verificar que el resultado es una lista de UserDto
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], UserDto)
    assert result[0].id == user_get["id"]
    assert result[0].username == user_get["username"]
    assert result[0].email == user_get["email"]
    assert result[0].role == user_get["role"]

    # Verificar que se llamó a get_users con el rol correcto
    mock_repo.get_users.assert_called_once_with(user_get["role"])

@pytest.mark.asyncio
async def test_list_users_empty():
    # Crear mocks
    mock_repo = AsyncMock()
    mock_repo.get_users.return_value = []  # Simular que no hay usuarios

    # Crear una instancia del servicio con el mock del repositorio
    service = GetUsers(mock_repo)

    # Ejecutar el método para listar los usuarios
    result = await service.list_users("customer")

    # Verificar que el resultado es una lista vacía
    assert isinstance(result, list)
    assert len(result) == 0

    # Verificar que se llamó a get_users con el rol correcto
    mock_repo.get_users.assert_called_once_with("customer")

@pytest.mark.asyncio
async def test_update_user_success(update_user_payload):
    # Crear un mock del repositorio
    mock_repo = AsyncMock()
    mock_repo.IsExistUserName.return_value = None  # Simular que el nombre de usuario no existe
    mock_repo.IsExistEmail.return_value = None  # Simular que el correo electrónico no existe

    # Simular que el usuario existe
    user_id = str(uuid4())
    user_aggregate = AggregateUser(id=user_id, user=MagicMock())
    user_aggregate.user.username = "existinguser"
    user_aggregate.user.email = "existing@example.com"
    user_aggregate.user.name = "Existing User"
    user_aggregate.user.role.value = "manager"
    user_aggregate.update = MagicMock()  # Simular la función update
    mock_repo.get_user_by_id.return_value = user_aggregate

    mock_repo.update_user.return_value = None  # Simular la actualización del usuario

    # Crear una instancia del servicio con el mock del repositorio
    service = UpdateUser(mock_repo)

    # Crear un DTO de usuario a partir de update_user_payload
    user_dto = UpdateUserDto(**update_user_payload)

    # Ejecutar el método para actualizar el usuario
    result = await service.update_user(user_id, user_dto)

    # Verificar que el resultado es True (usuario actualizado)
    assert result is True

   
@pytest.mark.asyncio
@patch("app.users.auth.utils.verify_password", return_value=True)
async def test_login_user_success(mock_verify_password, login_user_payload):
    # Crear un mock del repositorio
    mock_repo = AsyncMock()
    user_id = str(uuid4())
    hashed_password = get_password_hash("newpassword")
    user_model = User(id=user_id, username="johnupdated", password=hashed_password)
    mock_repo.IsExistUserName.return_value = user_model

    # Crear una instancia del servicio con el mock del repositorio
    service = LoginUser(mock_repo)

    # Crear un DTO de usuario a partir de login_user_payload
    user_dto = LoginUserDto(**login_user_payload)

    # Ejecutar el método para iniciar sesión
    result = await service.loginuser(user_dto)

    # Verificar que el resultado es un LoginRespuestaUserDto
    assert isinstance(result, LoginRespuestaUserDto)
    assert result.token_type == "bearer"

    # Decodificar el token para verificar su contenido
    decoded_token = jwt.decode(result.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == "johnupdated"
    assert decoded_token["exp"] > datetime.utcnow().timestamp()
