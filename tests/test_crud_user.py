import pytest
from unittest.mock import AsyncMock
from app.users.application.services.CreateUser import CreateUser
from app.users.application.dtos.CreateUserDto import CreateUserDto
from httpx import AsyncClient
from app.main import app

def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.asyncio
async def test_create_user_success(user_payload, db_session):
    mock_repo = AsyncMock()
    mock_repo.IsExistUserName.return_value = None
    mock_repo.IsExistEmail.return_value = None
    mock_repo.create_user.return_value = None

    user_dto = CreateUserDto(**user_payload)
    service = CreateUser(mock_repo)

    result = await service.create_user(user_dto)
    assert result is True

@pytest.mark.asyncio
async def test_login_user(test_client):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post(
            "/users/login",
            data={
                "grant_type": "password",
                "username": "superadmin",
                "password": "ContraSupAdmin123",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"