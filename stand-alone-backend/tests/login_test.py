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
from contextlib import contextmanager
from app.account_management import create_new_user, save_new_user


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


username = input("enter username: ")
password = input("enter password: ")

with get_db() as session:
    username, password = create_new_user(username, password, session)
    new_user = save_new_user(username, password, session)

    # Querying the database for the submitted user
    existing_user = session.query(models.User).filter(models.User.username == "user1").first()

if existing_user:
    username = existing_user.username
    hashed_password = existing_user.hashed_password
    print(f"Username: {username} and hashed_password: {hashed_password} have been saved to the database.")
else:
    print("Sign up failed, user is not saved in the database.")
