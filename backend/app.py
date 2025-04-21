from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
from models import UserDB, UserPublic
import os

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

client = AsyncIOMotorClient("mongodb://mongo:27017")
db = client["mydatabase"]
print('db', db)
users_collection = db["users"]
print('users_collection', users_collection)


@app.get("/")
def health_check():
    return {'message': 'Backend is working!'}

@app.get("/users", response_model=list[UserPublic])
async def get_users():
    users = []
    async for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

# @app.route("/users", methods=["POST"])
# def create_user():
#     data = request.get_json()
    
#     # Validate required fields
#     if not data.get('username') or not data.get('password'):
#         return jsonify({"error": "Username and password are required"}), 400
        
#     # Validate roles
#     valid_roles = {'admin', 'manager', 'tester'}
#     if any(role not in valid_roles for role in data.get('roles', [])):
#         return jsonify({"error": "Invalid role specified"}), 400

#     # Set timestamps
#     now = datetime.datetime.utcnow().timestamp()
#     data["created_ts"] = now
#     data["last_updated_ts"] = now
    
#     # Ensure preferences structure
#     data.setdefault('preferences', {'timezone': 'UTC'})
    
#     try:
#         result = users_collection.insert_one(data)
#         new_user = users_collection.find_one({"_id": result.inserted_id})
#         new_user["_id"] = str(new_user["_id"])
#         return jsonify(new_user), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# @app.route("/users/<user_id>", methods=["GET"])
# def get_user(user_id):
#     user = users_collection.find_one({"_id": ObjectId(user_id)})
#     if user:
#         user["_id"] = str(user["_id"])
#         user = convert_timestamps_to_iso(user)
#         return jsonify(user), 200
#     return jsonify({"error": "User not found"}), 404

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


