# type: ignore
import json
from dataclasses import dataclass
from datetime import datetime
from pymongo import MongoClient

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    active: bool = True
    created_ts: float = None

def parse_roles(user_data):
    roles = []
    if user_data.get('is_user_admin', False):
        roles.append("admin")
    if user_data.get('is_user_manager', False):
        roles.append("manager")
    if user_data.get('is_user_tester', False):
        roles.append("tester")
    return roles

def load_users_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    users = []
    for u in data.get("users", []):
        roles = parse_roles(u)
        # Convert ISO format (e.g., "2023-09-15T08:30:45Z") to Unix timestamp
        created_ts = datetime.strptime(u['created_at'], "%Y-%m-%dT%H:%M:%SZ").timestamp()
        preferences = UserPreferences(timezone=u['user_timezone'])
        user = User(
            username=u['user'],
            password=u['password'],
            roles=roles,
            preferences=preferences,
            active=u.get('is_user_active', True),
            created_ts=created_ts
        )
        users.append(user)
    return users

def insert_users_into_db(users):
    client = MongoClient("mongodb://mongo:27017/")
    db = client["mydatabase"]
    users_collection = db["users"]

    # If there is already any document in the collection, assume data was inserted before
    if users_collection.count_documents({}) > 0:
        print("Users already exist in the database. Skipping insertion.")
        return

    for user in users:
        user_document = {
            "username": user.username,
            "password": user.password,
            "roles": user.roles,
            "preferences": {"timezone": user.preferences.timezone},
            "active": user.active,
            "created_ts": user.created_ts,
        }
        users_collection.insert_one(user_document)
        print(f"Inserted user: {user.username}")

if __name__ == "__main__":
    users = load_users_from_json("udata.json")
    insert_users_into_db(users)
