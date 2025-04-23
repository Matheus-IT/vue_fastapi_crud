import pytest
from datetime import datetime, UTC


@pytest.mark.anyio
async def test_get_users_empty(async_client):
    response = await async_client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_create_and_get_user(async_client, users_collection):
    # Inserir diretamente na collection de teste
    await users_collection.insert_one(
        {
            "username": "tester",
            "roles": ["tester"],
            "preferences": {"timezone": "UTC"},
            "active": True,
            "created_ts": datetime.now(UTC),
            "last_updated_ts": None,
        }
    )
    response = await async_client.get("/users")
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "tester"
