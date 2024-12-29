import os
from uuid import uuid4
import pytest
import pytest_asyncio
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from fastapi.testclient import TestClient
from app.main import app
from app.users.infrastructure.db.database import get_session
from app.users.infrastructure.model.ModelUser import User
from app.users.auth.utils import get_password_hash

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
    # yield  # Ejecuta las pruebas
    # async with engine.begin() as conn:
    #     print("Dropping tables...")
    #     await conn.run_sync(SQLModel.metadata.drop_all)

# Fixture para crear un usuario superadmin
@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_superadmin():
    async with engine.begin() as conn:
        session = async_session(bind=conn)
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

# Fixture para crear una sesión de base de datos para cada prueba
@pytest.fixture(scope="function")
async def db_session():
    async with engine.connect() as connection:
        async with connection.begin() as transaction:
            session = async_session(bind=connection)
            yield session
            await session.close()
    

# Fixture para crear un cliente de prueba
@pytest.fixture(scope="function")
def test_client(db_session):
    """Crea un cliente de prueba que establece como función de reemplazo override_get_db para la sesión de pruebas."""

    async def override_get_db():
        try:
            yield db_session
        finally:
            await db_session.aclose()

    app.dependency_overrides[get_session] = override_get_db
    client = TestClient(app)
    yield client

@pytest.fixture
def user_payload():
    return {
        "name": "John",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "password",
        "role": "manager"
    }

