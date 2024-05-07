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

from selenium import webdriver
from selenium.webdriver.common.by import By
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


driver = webdriver.Firefox()
port = 8000
driver.get(f"http://127.0.0.1:{port}/")

username_field = driver.find_element(By.NAME, "username")
password_field = driver.find_element(By.NAME, "password")
submit_button = driver.find_element(By.ID, "submit")

username_field.send_keys("user1")
password_field.send_keys("foo")
submit_button.click()

# Waiting for the page to load
driver.implicitly_wait(5)

print(driver.current_url)

# Querying the database for the submitted user
with get_db() as db:
    existing_user = db.query(models.User).filter(models.User.username == "user1").first()

if existing_user:
    username = existing_user.username
    hashed_password = existing_user.hashed_password
    print(f"Username: {username} and hashed_password: {hashed_password} have been saved to the database.")
else:
    print("Sign up failed, user is not saved in the database.")

driver.quit()
