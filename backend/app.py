from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os

app = Flask(__name__)
CORS(app)

# Load connection info from environment variables (optional)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)
db = client["mydatabase"]
users_collection = db["users"]

@app.route("/", methods=["GET"])
def home():
    return {'message': 'Backend is working!'}

@app.route("/users", methods=["GET"])
def get_users():
    users = []
    for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return jsonify(users), 200

@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    # Set timestamps for created and updated times
    now = datetime.datetime.utcnow().timestamp()
    data["created_ts"] = now
    data["last_updated_ts"] = now
    result = users_collection.insert_one(data)
    new_user = users_collection.find_one({"_id": result.inserted_id})
    new_user["_id"] = str(new_user["_id"])
    return jsonify(new_user), 201

@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    data["last_updated_ts"] = datetime.datetime.utcnow().timestamp()
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    if result.modified_count:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    return jsonify({"error": "User not found or no changes made"}), 404

@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
