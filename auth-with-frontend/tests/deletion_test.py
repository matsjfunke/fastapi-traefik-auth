"""
matsjfunke
07.05.2024
"""
import os
import sys

# Add the parent directory of the current file to the Python path for app imports to work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.db.database import SessionLocal
from app.db import models
from app.account_management import delete_user
from contextlib import contextmanager


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


username = "user2"

with get_db() as db:
    delete_user(username, db)

# Querying the database for the deleted user
with get_db() as db:
    existing_user = db.query(models.User).filter(models.User.username == username).first()

if existing_user:
    to_delete_user = existing_user.username
    hashed_password = existing_user.hashed_password
    print(f"Username: {username} still in the database.")
else:
    print(f"User {username} has been deleted from the database.")
