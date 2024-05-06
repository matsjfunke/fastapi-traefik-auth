"""
matsjfunke
"""
import os
from datetime import timedelta

from fastapi import FastAPI, Form, HTTPException, Request, status, Query
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

# authentication imports
from .authentication import authenticate_user, create_access_token, vaildate_cookies, ACCESS_TOKEN_EXPIRE_MINUTES, json_db
from fastapi.security import OAuth2PasswordBearer

# sgin-up imports
from .account_creation import hash_password


app = FastAPI()


# Initialize template directory relative to the current file location
current_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/sign-up", response_class=HTMLResponse)
async def sign_up_form(request: Request):
    print("get sign-up")
    return templates.TemplateResponse("sign-up.html", {"request": request})


@app.post("/sign-up")
async def create_account(username: str = Form(...), password: str = Form(...)):
    hash = hash_password(password)
    return {"hash_password": hash}


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
