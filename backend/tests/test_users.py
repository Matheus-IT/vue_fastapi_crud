import pytest
from datetime import datetime, timezone, UTC
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId


# testando rotas que retornam usuários ========================================
@pytest.mark.anyio
async def test_get_users_empty(async_client):
    response = await async_client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_get_single_user(async_client, users_collection):
    # Inserir diretamente na collection de teste
    await users_collection.insert_one(
        {
            "username": "tester",
            "roles": ["tester"],
            "preferences": {"timezone": "UTC"},
            "active": True,
            "created_ts": datetime.now(UTC).isoformat(),
            "last_updated_ts": None,
        }
    )
    response = await async_client.get("/users")
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "tester"


# testando a criação de usuários ==============================================
@pytest.mark.anyio
async def test_create_user(async_client, users_collection):
    payload = {
        "username": "tester",
        "password": "123",
        "roles": ["tester"],
        "preferences": {"timezone": "UTC"},
        "active": True,
        "created_ts": datetime.now(UTC).isoformat(),
        "last_updated_ts": None,
    }
    response = await async_client.post("/users", json=payload)
    data = response.json()
    assert data["username"] == "tester"


@pytest.mark.anyio
async def test_create_user_last_updated_at_none(async_client):
    payload = {
        "username": "withnone",
        "password": "123",
        "roles": ["tester"],
        "preferences": {"timezone": "UTC"},
        "last_updated_at": None,
    }
    response = await async_client.post("/users", json=payload)
    data = response.json()
    assert response.status_code == 200
    assert data["last_updated_at"] is None


@pytest.mark.anyio
async def test_create_user_with_min_params(async_client, users_collection):
    """
    Testa a criação de um usuário com os parâmetros mínimos necessários.
    """
    payload = {
        "username": "tester",
        "password": "123",
        "roles": ["tester"],
        "preferences": {"timezone": "UTC"},
    }
    response = await async_client.post("/users", json=payload)
    data = response.json()
    assert data["username"] == "tester"
    assert data["active"] is True
    assert data["created_at"] is not None
    assert data["last_updated_at"] is None


@pytest.mark.anyio
async def test_create_user_with_all_fields(async_client, users_collection):
    payload = {
        "username": "fulluser",
        "password": "123",
        "roles": ["admin", "manager"],
        "preferences": {"timezone": "America/Sao_Paulo"},
        "active": False,
        "last_updated_at": "2024-01-01T12:00:00Z",
    }
    response = await async_client.post("/users", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["username"] == "fulluser"
    assert data["active"] is False
    assert data["roles"] == ["admin", "manager"]
    assert data["preferences"]["timezone"] == "America/Sao_Paulo"
    assert data["last_updated_at"] is not None


@pytest.mark.anyio
async def test_create_user_invalid_datetime(async_client):
    payload = {
        "username": "badtime",
        "password": "123",
        "roles": ["tester"],
        "preferences": {"timezone": "UTC"},
        "last_updated_at": "not-a-datetime",
    }
    response = await async_client.post("/users", json=payload)
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["type"] == "datetime_from_date_parsing"


@pytest.mark.anyio
async def test_create_user_with_invalid_roles(async_client):
    payload = {
        "username": "invalid_roles",
        "password": "123",
        "roles": "admin",  # Should be a list!
        "preferences": {"timezone": "UTC"},
    }
    response = await async_client.post("/users", json=payload)
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["type"] == "list_type"


@pytest.mark.anyio
async def test_create_user_missing_username(async_client):
    payload = {
        "roles": ["viewer"],
        "preferences": {"timezone": "UTC"},
    }
    response = await async_client.post("/users", json=payload)
    assert response.status_code == 422


@pytest.fixture
def mock_users_collection_with_error(mocker):
    """
    Fixture to mock the users_collection with an insert_one method that raises an exception.
    """
    mock_users_collection = mocker.MagicMock()
    mock_users_collection.insert_one = AsyncMock(
        side_effect=Exception("Database error")
    )
    mock_users_collection.update_one = AsyncMock(
        side_effect=Exception("Database error")
    )
    return mock_users_collection


@pytest.fixture
def override_users_collection_with_error(mock_users_collection_with_error):
    """
    Before the test: override get_users_collection → mock that always errors.
    After the test: clear all overrides.
    """
    from app.database import get_users_collection
    from app.main import app

    app.dependency_overrides[get_users_collection] = (
        lambda: mock_users_collection_with_error
    )
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_create_user_db_error(async_client, override_users_collection_with_error):
    payload = {
        "username": "db_error",
        "password": "123",
        "roles": ["admin"],
        "preferences": {"timezone": "UTC"},
    }

    response = await async_client.post("/users", json=payload)
    data = response.json()

    assert response.status_code == 500  # or another code if you prefer
    assert "detail" in data
    assert "Database error" in data["detail"]


# testando retorno de único usuário ===========================================
@pytest.mark.anyio
async def test_get_user(async_client, users_collection):
    # Inserir diretamente na collection de teste
    await users_collection.insert_one(
        {
            "username": "tester",
            "roles": ["tester"],
            "preferences": {"timezone": "UTC"},
            "active": True,
            "created_ts": datetime.now(UTC).isoformat(),
            "last_updated_ts": None,
        }
    )
    tester_id = (await users_collection.find_one({"username": "tester"}))["_id"]
    response = await async_client.get(f"/users/{tester_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == "tester"


@pytest.mark.anyio
async def test_get_user_not_found(async_client, users_collection):
    response = await async_client.get(f"/users/000000000000000000000000")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "User not found"


# testando atualização de usuário ==========================================
@pytest.mark.anyio
async def test_update_user_success(
    async_client,
    mock_users_collection_with_error,
    override_users_collection_with_error,
):
    # Arrange
    user_id = ObjectId()
    # Simulate update_one modified 1 doc
    mock_users_collection_with_error.update_one = AsyncMock(
        return_value=MagicMock(modified_count=1)
    )
    # Simulate fetching the updated doc
    fake_doc = {
        "_id": user_id,
        "username": "bob",
        "roles": ["tester"],
        "preferences": {"timezone": "UTC"},
        "active": False,
        "created_at": datetime.now(timezone.utc),
        "last_updated_at": None,
    }
    mock_users_collection_with_error.find_one = AsyncMock(return_value=fake_doc)

    payload = {"username": "bob", "active": False}

    # Act
    response = await async_client.patch(f"/users/{user_id}", json=payload)
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["username"] == "bob"
    assert data["active"] is False


@pytest.mark.anyio
async def test_update_user_not_found_valid_id(
    async_client, mock_users_collection_with_error
):
    # Arrange: no document modified
    mock_users_collection_with_error.update_one = AsyncMock(
        return_value=MagicMock(modified_count=0)
    )

    # Act
    response = await async_client.patch(
        "/users/000000000000000000000000", json={"active": True}
    )
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data == {"detail": "User not found"}


@pytest.mark.anyio
async def test_update_user_malformed_id(async_client):
    # Act
    response = await async_client.patch("/users/invalid-id-123", json={"active": True})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@pytest.mark.anyio
async def test_update_user_no_fields(async_client):
    # Act: empty body
    response = await async_client.patch(f"/users/{ObjectId()}", json={})
    data = response.json()

    # Assert
    assert response.status_code == 422
    assert "No fields provided to update" in data["detail"]


@pytest.mark.anyio
async def test_update_user_db_error(
    async_client, users_collection, override_users_collection_with_error
):
    await users_collection.insert_one(
        {
            "username": "tester",
            "roles": ["tester"],
            "preferences": {"timezone": "UTC"},
            "active": True,
            "created_ts": datetime.now(UTC).isoformat(),
            "last_updated_ts": None,
        }
    )
    tester_id = (await users_collection.find_one({"username": "tester"}))["_id"]
    # Act
    response = await async_client.patch(f"/users/{tester_id}", json={"active": True})
    data = response.json()

    # Assert
    assert response.status_code == 500
    assert data["detail"] == "Database error"


@pytest.mark.anyio
async def test_update_user_invalid_roles_type(async_client):
    # Act: roles must be list
    payload = {"roles": "not-a-list"}
    response = await async_client.patch(f"/users/{ObjectId()}", json=payload)
    data = response.json()

    # Assert
    assert response.status_code == 422
    # Pydantic list_type error
    assert data["detail"][0]["type"] == "list_type"


# testando exclusão de usuário ==========================================
@pytest.mark.anyio
async def test_delete_user_success(
    async_client, mock_users_collection_with_error, override_users_collection_with_error
):
    # Arrange: delete_one returns a SimpleNamespace with deleted_count=1
    mock_users_collection_with_error.delete_one = AsyncMock(
        return_value=MagicMock(deleted_count=1)
    )

    # Act
    user_id = ObjectId()
    response = await async_client.delete(f"/users/{user_id}")

    # Assert
    assert response.status_code == 204  # No Content


@pytest.mark.anyio
async def test_delete_user_not_found_valid_id(async_client):
    # Act
    response = await async_client.delete("/users/000000000000000000000000")
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data == {"detail": "User not found"}


@pytest.mark.anyio
async def test_delete_user_malformed_id(async_client):
    # Act: pass a non-hex string
    response = await async_client.delete("/users/invalid-id-123")
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data == {"detail": "User not found"}


@pytest.mark.anyio
async def test_delete_user_db_error(
    async_client, mock_users_collection_with_error, override_users_collection_with_error
):
    # Arrange: simulate a database exception
    mock_users_collection_with_error.delete_one = AsyncMock(
        side_effect=Exception("Database error")
    )

    # Act
    response = await async_client.delete(f"/users/{ObjectId()}")
    data = response.json()

    # Assert
    assert response.status_code == 500
    assert data["detail"] == "Database error"
