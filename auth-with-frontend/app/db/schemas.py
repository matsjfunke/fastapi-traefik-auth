"""
matsjfunke

Pydantic models used for data validation, serialization, and deserialization.
"""
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
