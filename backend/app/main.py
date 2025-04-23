from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_users_collection
from app.models import UserPublic, UserDBCreate
from motor.motor_asyncio import AsyncIOMotorCollection

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
    from bson import ObjectId

    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        print("\nici!!!")
        raise HTTPException(detail="User not found", status_code=404)

    user["_id"] = str(user["_id"])
    return user


# @app.route("/users/<user_id>", methods=["PUT"])
# def update_user(user_id):
#     data = request.get_json()
#     data["last_updated_ts"] = datetime.datetime.utcnow().timestamp()
#     result = users_collection.update_one(
#         {"_id": ObjectId(user_id)},
#         {"$set": data}
#     )
#     if result.modified_count:
#         updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
#         updated_user["_id"] = str(updated_user["_id"])
#         updated_user = convert_timestamps_to_iso(updated_user)
#         return jsonify(updated_user), 200
#     return jsonify({"error": "User not found or no changes made"}), 404

# @app.route("/users/<user_id>", methods=["DELETE"])
# def delete_user(user_id):
#     result = users_collection.delete_one({"_id": ObjectId(user_id)})
#     if result.deleted_count:
#         return jsonify({"message": "User deleted"}), 200
#     return jsonify({"error": "User not found"}), 404
