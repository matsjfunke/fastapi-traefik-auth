"""
matsjfunke
07.05.2024
"""
from app.db.database import SessionLocal
from app.db import models
from contextlib import contextmanager


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Querying the database for the submitted user
with get_db() as db:
    existing_user = db.query(models.User).filter(models.User.username == "user1").first()

if existing_user:
    username = existing_user.username
    hashed_password = existing_user.hashed_password
    print(f"Username: {username} and hashed_password: {hashed_password} have been saved to the database.")
else:
    print("Sign up failed, user is not saved in the database.")
