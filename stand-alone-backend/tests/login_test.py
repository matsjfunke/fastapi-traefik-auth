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
from app.authentication import authenticate_user


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
    authenticated_username = authenticate_user(username, password, session)
    if username is None:
        print("Incorrect username or password")

    # Querying the database for the submitted user
    existing_user = session.query(models.User).filter(models.User.username == "user1").first()

if existing_user:
    print("user {username} is loggined in")
else:
    print("Login failed, user is not saved in the database.")
