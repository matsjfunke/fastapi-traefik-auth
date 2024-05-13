"""
Mats Funke
24.03.2024
"""
import os

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Union

from fastapi import HTTPException, status

from .db import models
from sqlalchemy.orm import Session


SECRET_KEY = os.environ.get("auth_secret_key")
ALGORITHM = "HS256"
# TODO: Consider implementing refresh tokens to obtain access without re-authenticating
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def user_lookup(username: str, session: Session):
    existing_user = session.query(models.User).filter(models.User.username == username).first()

    if existing_user:
        username = existing_user.username
        hashed_password = existing_user.hashed_password
        return username, hashed_password
    else:
        return None


# pwd_context.verify is designed to resist timing attacks by taking a constant time regardless of whether the password matches or not
def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def authenticate_user(username: str, password: str, session: Session):
    username, hashed_password = user_lookup(username, session)
    if username and verify_password(password, hashed_password):
        return username

    return None


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def vaildate_cookies(access_token):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no cookies, in your jar",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
