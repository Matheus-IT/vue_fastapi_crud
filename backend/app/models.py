from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


RoleType = Literal["admin", "manager", "tester"]


class UserPreferences(BaseModel):
    timezone: str


class UserPublic(BaseModel):
    id: str = Field(
        serialization_alias="id", validation_alias="_id"
    )  # mongodb default id field
    username: str
    roles: list[RoleType]
    preferences: UserPreferences
    active: bool = True
    created_at: datetime = Field(
        serialization_alias="created_at", validation_alias="created_ts"
    )
    last_updated_at: datetime | None = Field(
        default=None,
        serialization_alias="last_updated_at",
        validation_alias="last_updated_ts",
    )


class UserDBCreate(BaseModel):
    username: str
    roles: list[RoleType]
    preferences: UserPreferences
    active: bool = True
    created_at: datetime = Field(
        serialization_alias="created_ts", validation_alias="created_at"
    )
    last_updated_at: datetime | None = Field(
        default=None,
        serialization_alias="last_updated_ts",
        validation_alias="last_updated_at",
    )


class UserDB(UserPublic):
    id: str = Field(
        serialization_alias="_id", validation_alias="id"
    )  # mongodb default id field
