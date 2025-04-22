from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends


def get_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient("mongodb://mongo:27017")


async def get_users_collection(
    client: AsyncIOMotorClient = Depends(get_mongo_client),
):
    db = client["mydatabase"]
    yield db["users"]
