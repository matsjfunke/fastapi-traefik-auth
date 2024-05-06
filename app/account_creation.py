"""
matsjfunke
"""
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from .db.models import User
from .db.schemas import UserCreate
from .db.database import SessionLocal


def hash_password(plain_password):
    """uses pwd_context to encrypt the plain_password from the /sign-up html from"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(plain_password)
    return hashed_password


def create_user(user: UserCreate, db: Session):
    db_user = User(username=user.username, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
