"""
matsjfunke
"""
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
from .account_creation import hash_password
from .db import models, database
from .db.schemas import User
from sqlalchemy.orm import Session
from typing import List


app = FastAPI()


# Initialize template directory relative to the current file location
current_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create the tables
models.Base.metadata.create_all(bind=database.engine)


@app.get("/", response_class=HTMLResponse)
async def sign_up_form(request: Request):
    print("get sign-up")
    return templates.TemplateResponse("sign-up.html", {"request": request})


@app.post("/sign-up")
async def create_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password
    hashed_password = hash_password(password)

    # Create user in the database
    new_user = models.User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# Endpoint to get all users
@app.get("/users/", response_model=List[User])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
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
    print("Status Code:", response.status_code)
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
