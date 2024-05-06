"""
matsjfunke
"""
from passlib.context import CryptContext


def hash_password(plain_password):
    """uses pwd_context to encrypt the plain_password from the /sign-up html from"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(plain_password)
    return hashed_password
