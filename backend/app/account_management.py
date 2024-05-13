"""
matsjfunke
"""
# hash_password import
from passlib.context import CryptContext


import re
from .db import models
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError
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
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters long")
    if len(password) < 3:
        raise HTTPException(status_code=400, detail="Password must be at least 3 characters long")

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


def update_username(existing_username: str, new_username: str, session: Session):
    try:
        # Check if the existing username exists in the database
        user_to_update = session.query(models.User).filter_by(username=existing_username).one()
        # Update the username
        user_to_update.username = new_username
        session.commit()
        return {"status": 200, "detail": f"Username: {existing_username} was updated to {new_username}"}
    except NoResultFound:
        return {"status": 400, "detail": f"The user: {existing_username} you are trying to update doesn't exist"}
    except IntegrityError:
        session.rollback()  # Rollback the session to avoid leaving it in an inconsistent state
        return {"status": 400, "detail": f"Failed to update username. The new username '{new_username}' is already taken."}


def delete_user(username: str, session: Session):
    try:
        user_to_delete = session.query(models.User).filter_by(username=username).one()
        session.delete(user_to_delete)
        session.commit()
        return {"status": 200, "detail": f"user: {username} was deleted"}
    except NoResultFound:
        return {"status": 400, "detail": f"failed to delete user: {username}"}
