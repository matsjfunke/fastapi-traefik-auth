"""
matsjfunke
"""
from datetime import timedelta
from typing import List

from fastapi import FastAPI, Form, Request, Response, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# authentication imports
from .authentication import authenticate_user, create_access_token, vaildate_cookies, ACCESS_TOKEN_EXPIRE_MINUTES

# database related imports
from .account_management import create_new_user, save_new_user, update_username, delete_user
from .db import models, database
from .db.schemas import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager


app = FastAPI()


# allow the frontend to access endpoints
origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Dependency to get the database session
@contextmanager
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        db.rollback()
    finally:
        # Close the session to release resources
        db.close()


# Create the tables on startup
models.Base.metadata.create_all(bind=database.engine)


# API endpoint for signing up
@app.post("/sign-up")
async def sign_up(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    print("creating account...")
    with db as session:
        username, password = create_new_user(username, password, session)
        new_user = save_new_user(username, password, session)

    print(f"saved user {new_user.username} with ID {new_user.id} to db\n")
    return RedirectResponse("/login")


# API endpoint for logging in and cookie creating
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    print(f"authenticating user: {username}")

    with db as session:
        auth_username = authenticate_user(username, password, session)
        if auth_username is None:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
            )
        access_token = create_access_token(data={"sub": username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

        redirect_url = f"/hello?username={username}"
        response = RedirectResponse(redirect_url)
        response.set_cookie(key="access_token", value=access_token)

        print(f"user: {auth_username} is logged in, with token: {access_token}\n")
        return response


# Endpoint to get all users
@app.get("/users/", response_model=List[User])
async def get_all_users(request: Request, db: Session = Depends(get_db)):

    # vaildate_cookies protects this endpoint
    vaildate_cookies(request.cookies.get("access_token"))

    with db as session:
        users = session.query(models.User).all()
        return users


# Update username endpoint
@app.post("/update-username")
async def update_username_in_db(request: Request, old_username: str = Form(...), new_username: str = Form(...), db: Session = Depends(get_db)):

    # vaildate_cookies protects this endpoint
    vaildate_cookies(request.cookies.get("access_token"))

    with db as session:
        status = update_username(old_username, new_username, session)
        print(status, "\n")

    return RedirectResponse(f"/hello?username={new_username}")


# Delete user endpoint
@app.post("/delete-user")
async def delete_user_in_db(request: Request, response: Response, username: str = Form(...), db: Session = Depends(get_db)):

    # vaildate_cookies protects this endpoint
    vaildate_cookies(request.cookies.get("access_token"))

    with db as session:
        status = delete_user(username, session)
        print(status, "\n")

    response.delete_cookie("access_token")

    return RedirectResponse("/login")
