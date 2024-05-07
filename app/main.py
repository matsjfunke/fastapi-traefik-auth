"""
matsjfunke
"""
import os
from datetime import timedelta
from typing import List

from fastapi import FastAPI, Form, HTTPException, Request, status, Query, Depends, Response
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette import status

from fastapi.templating import Jinja2Templates

# authentication imports
from .authentication import authenticate_user, create_access_token, vaildate_cookies, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer

# database related imports
from .account_management import create_new_user, save_new_user, update_username, delete_user
from .db import models, database
from .db.schemas import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
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
        print(f"Database error: {e}")
        db.rollback()
    finally:
        # Close the session to release resources
        db.close()


# Create the tables on startup
models.Base.metadata.create_all(bind=database.engine)


@app.get("/", response_class=HTMLResponse)
async def sign_up_form(request: Request):
    print("get sign-up")
    return templates.TemplateResponse("sign-up.html", {"request": request})


@app.post("/sign-up")
async def create_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    print("creating account...")
    with db as session:
        username, password = create_new_user(username, password, session)
        new_user = save_new_user(username, password, session)
    print(f"saved user {new_user.username} with ID {new_user.id} to db\n")
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    print("get login")
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def authentication_cookie_creation(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    print("post login")
    with db as session:
        username = authenticate_user(username, password, session)
        if username is None:
            print("login failed incorrect username or output")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        print("login successful, cookie created")

        # set url here:
        redirect_url = f"/hello?username={username}"

        response = RedirectResponse(url=redirect_url, status_code=status.HTTP_308_PERMANENT_REDIRECT)
        response.set_cookie(key="access_token", value=access_token)

        print("Redirect URL:", response.headers["location"])
        print(f"Status Code: {response.status_code}\n")
    return response


# without post now refresh
@app.get("/hello")
@app.post("/hello")
async def hello(request: Request, username: str = Query(...)):
    # authenticate users cookies
    vaildate_cookies(request.cookies.get("access_token"))

    # just for output
    access_token = request.cookies.get("access_token")
    return templates.TemplateResponse("hello.html", {"request": request, "username": username, "access_token": access_token})


# Endpoint to get all users
@app.get("/users/", response_model=List[User])
async def get_all_users(request: Request, db: Session = Depends(get_db)):
    vaildate_cookies(request.cookies.get("access_token"))

    # Use the database session within a 'with' statement
    with db as session:
        users = session.query(models.User).all()
        return users


@app.post("/update_username")
async def update_username_in_db(request: Request, old_username: str = Form(...), new_username: str = Form(...), db: Session = Depends(get_db)):
    vaildate_cookies(request.cookies.get("access_token"))

    with db as session:
        update_username(old_username, new_username, session)
        print(f"updated username: {old_username} to {new_username}")

        redirect_url = f"hello?username={new_username}"
    return RedirectResponse(redirect_url)


@app.post("/delete_user")
async def delete_user_credentails(request: Request, response: Response, username: str = Form(...), db: Session = Depends(get_db)):
    vaildate_cookies(request.cookies.get("access_token"))

    with db as session:
        status = delete_user(username, session)
        print(f"deleted user {username}")

    response.delete_cookie("access_token")
    return status
