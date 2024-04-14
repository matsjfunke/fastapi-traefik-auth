"""
Mats Funke
01.03.2024
"""
import json
import os

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union

SECRET_KEY = os.environ.get("auth_secret_key")
ALGORITHM = "HS256"
# TODO: Consider implementing refresh tokens to obtain access without re-authenticating
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


with open("app/user_db.json", "r") as file:
    json_db = json.load(file)


def user_lookup(username, json_db):
    for entry in json_db["db"]:
        if entry["username"] == username:
            return entry
    return None


# pwd_context.verify is designed to resist timing attacks by taking a constant time regardless of whether the password matches or not
def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def authenticate_user(username, password, json_db):
    user_entry = user_lookup(username, json_db)
    if user_entry and verify_password(password, user_entry["hashed_password"]):
        return user_entry

    return None


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
