from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_users_collection
from app.models import UserPublic, UserDBCreate, UserUpdate
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"message": "Backend is working!"}


@app.get("/users", response_model=list[UserPublic])
async def get_users(users_collection=Depends(get_users_collection)):
    users = []
    async for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users


@app.post("/users", response_model=UserPublic)
async def create_user(
    user: UserDBCreate,
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection),
):
    data = user.model_dump()

    # convert to timestamps for db
    data["created_at"] = data["created_at"].timestamp()
    if data["last_updated_at"]:
        data["last_updated_at"] = data["last_updated_at"].timestamp()
    print("data", data)

    try:
        result = await users_collection.insert_one(data)
        new_user = await users_collection.find_one({"_id": result.inserted_id})
        new_user["_id"] = str(new_user["_id"])
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}", response_model=UserPublic)
async def get_user(
    user_id: str,
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection),
):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        print("\nici!!!")
        raise HTTPException(detail="User not found", status_code=404)

    user["_id"] = str(user["_id"])
    return user


@app.patch("/users/{user_id}", response_model=UserPublic)
async def update_user(
    user_id: str,
    update: UserUpdate,
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection),
):
    try:
        oid = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(
            status_code=404, detail="User not found"
        )  # malformed IDs → 404

    # Build update dict, excluding values that were not provided
    data = update.model_dump(exclude_none=True)
    # Convert datetime fields to timestamps
    for dt_field in ("created_at", "last_updated_at"):
        if dt_field in data and isinstance(data[dt_field], datetime):
            data[dt_field] = data[dt_field].timestamp()

    if not data:
        raise HTTPException(status_code=422, detail="No fields provided to update")

    try:
        result = await users_collection.update_one({"_id": oid}, {"$set": data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    user = await users_collection.find_one({"_id": oid})
    user["_id"] = str(user["_id"])
    return user


@app.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: str,
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection),
):
    try:
        oid = ObjectId(user_id)
    except InvalidId:
        # malformed ID → not found
        raise HTTPException(status_code=404, detail="User not found")

    try:
        result = await users_collection.delete_one({"_id": oid})
    except Exception as e:
        # database failure → 500
        raise HTTPException(status_code=500, detail=str(e))

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return
