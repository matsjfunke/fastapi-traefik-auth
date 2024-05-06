"""
matsjfunke
"""
import re
import os
from datetime import timedelta

from fastapi import FastAPI, Form, HTTPException, Request, status, Query, Depends
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

# authentication imports
from .authentication import authenticate_user, create_access_token, vaildate_cookies, ACCESS_TOKEN_EXPIRE_MINUTES, json_db
from fastapi.security import OAuth2PasswordBearer

# account creation imports
from .account_creation import create_new_user, save_new_user
from .db import models, database
from .db.schemas import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from contextlib import contextmanager

app = FastAPI()


# Initialize template directory relative to the current file location
current_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency to get the database session
@contextmanager
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        # Handle the exception, log it, or perform any necessary cleanup
        print(f"Database error: {e}")
        # Rollback the transaction if needed
        db.rollback()
    finally:
        # Close the session to release resources
        db.close()


# Create the tables
models.Base.metadata.create_all(bind=database.engine)


@app.get("/", response_class=HTMLResponse)
async def sign_up_form(request: Request):
    print("get sign-up")
    return templates.TemplateResponse("sign-up.html", {"request": request})


@app.post("/sign-up")
async def create_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    print("creating account...")
    with db as session:
        username, password = create_new_user(username, password, session)
        new_user = save_new_user(username, password, session)
    print("saved user to db\n")
    return {"message": "User created successfully", "user": new_user}


# Endpoint to get all users
@app.get("/users/", response_model=List[User])
async def get_all_users(db: Session = Depends(get_db)):
    # Use the database session within a 'with' statement
    with db as session:
        users = session.query(models.User).all()
        return users


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    print("get login")
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    print("post login")
    user = authenticate_user(username, password, json_db)
    if user is None:
        print("login failed incorrect username or output")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    print("login successful, cookie created")

    # set url here:
    redirect_url = f"/hello?username={username}"

    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_308_PERMANENT_REDIRECT)
    response.set_cookie(key="access_token", value=access_token)

    print("Response content before returning: ", response)
    print("Redirect URL:", response.headers["location"])
    print(f"Status Code: {response.status_code}\n")
    return response


# without post now refresh
@app.get("/hello")
@app.post("/hello")
def hello(request: Request, username: str = Query(...)):
    # authentication part
    vaildate_cookies(request.cookies.get("access_token"))

    # just for output
    access_token = request.cookies.get("access_token")
    return templates.TemplateResponse("hello.html", {"request": request, "username": username, "access_token": access_token})
