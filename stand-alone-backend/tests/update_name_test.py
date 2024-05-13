"""
matsjfunke
13.05.2024
"""
import os
import sys

# Add the parent directory of the current file to the Python path for app imports to work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.db.database import SessionLocal
from app.db import models
from app.account_management import update_username
from contextlib import contextmanager


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


existing_username = "user1"
new_username = "user1"

with get_db() as db:
    result = update_username(existing_username, new_username, db)
    print(result.detail)

if result.status_code == 200:
    # Querying the database for the updated user
    with get_db() as db:
        new_user = db.query(models.User).filter(models.User.username == new_username).first()

    if new_user:
        print(f"Username: {existing_username} was replaced with {new_user.username}")
