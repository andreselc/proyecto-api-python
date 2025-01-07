import os
import pytest
import pytest_asyncio
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from fastapi.testclient import TestClient
from app.main import app
from app.users.infrastructure.db.database import get_session
from app.common.infrastructure.Modelo import User
from app.users.auth.utils import get_password_hash
from datetime import datetime
from uuid import uuid4

# Importar la función get_session de la aplicación
DATABASE_URL = os.environ.get("DATABASE_URL_TEST")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)
# Crear una sesión de prueba
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Fixture para inicializar la base de datos y crear las tablas
@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_database():
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(SQLModel.metadata.create_all)
    yield  # Ejecuta las pruebas
    async with engine.begin() as conn:
        print("Dropping tables...")
        await conn.run_sync(SQLModel.metadata.drop_all)


# Fixture para crear una sesión de base de datos para cada prueba
@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with async_session() as session:
        yield session

# Fixture para crear un usuario superadmin
@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_superadmin():
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == "superadmin"))
        superadmin_user = result.scalar_one_or_none()
        if not superadmin_user:
            user = User(
                name="Superadmin",
                email="superadmin@example.com",
                username="superadmin",
                password=get_password_hash("superadmin_password"),
                role="superadmin"
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
    
# Fixture para crear un cliente de prueba
@pytest.fixture(scope="function")
def test_client(db_session):
    async def override_get_db():
        try:
            yield db_session
        finally:
            await db_session.aclose()

    app.dependency_overrides[get_session] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
def user_payload():
    return {
        "name": "John",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "password",
        "role": "manager"
    }

@pytest.fixture
def user_get():
    return {
        "id": str(uuid4()),
        "name": "Johnnathan",
        "email": "prueba@example.com",
        "username": "jhonny",
        "password": "12345",
        "role": "customer",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    }

@pytest.fixture
def update_user_payload():
    return {
        "name": "John Updated",
        "email": "john.updated@example.com",
        "username": "johnupdated",
        "password": "newpassword"
    }

@pytest.fixture
def login_user_payload():
    return {
        "username": "johnupdated",
        "password": "newpassword"
    }
