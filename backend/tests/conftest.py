import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from mongomock_motor import AsyncMongoMockClient
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import get_mongo_client, get_users_collection


@pytest.fixture(scope="session")
def anyio_backend():
    """Loop de evento para testes async"""
    return "asyncio"  # para pytest-asyncio


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_mongo_client(monkeypatch):
    """Mock do MongoDB in-memory"""
    mock_client = AsyncMongoMockClient()
    monkeypatch.setattr("app.database.get_mongo_client", lambda: mock_client)
    return mock_client


@pytest.fixture
async def users_collection(mock_mongo_client):
    """Fixture para collection de usuários usando o mock"""
    db = mock_mongo_client["test_database"]
    return db["users"]

# 5) Override das dependências no app
@pytest.fixture(autouse=True)
def override_dependencies(mock_mongo_client):
    app.dependency_overrides[get_mongo_client] = lambda: mock_mongo_client
    app.dependency_overrides[get_users_collection] = lambda: mock_mongo_client["test_database"]["users"]
    yield
    app.dependency_overrides.clear()
