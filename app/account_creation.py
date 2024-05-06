"""
matsjfunke
"""
# hash_password import
from passlib.context import CryptContext


import re
from .db import models
from sqlalchemy.orm import Session
from fastapi import HTTPException


def hash_password(plain_password):
    """uses pwd_context to encrypt the plain_password from the /sign-up html from"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(plain_password)
    return hashed_password


USERNAME_REGEX = r'^[^\W_][\w]*$'


def create_new_user(username: str, password: str, session: Session):
    # Duplicate validation
    existing_user = session.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Length validation
    if len(username) < 4:
        raise HTTPException(status_code=400, detail="Username must be at least 4 characters long")
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")

    # Validation of username format
    if not re.match(USERNAME_REGEX, username):
        raise HTTPException(status_code=400, detail="Username contains invalid characters")

    return username, password


def save_new_user(username: str, password: str, session: Session):
    hashed_password = hash_password(password)
    new_user = models.User(username=username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
