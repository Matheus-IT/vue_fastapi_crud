from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


RoleType = Literal["admin", "manager", "tester"]


class UserPreferences(BaseModel):
    timezone: str


class UserPublic(BaseModel):
    id: str = Field(alias="_id", serialization_alias="id")  # mongodb default id field
    username: str
    roles: list[RoleType]
    preferences: UserPreferences
    active: bool = True
    created_at: datetime = Field(alias="created_ts", serialization_alias="created_at")


class UserDB(UserPublic):
    password: str
