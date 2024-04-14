"""
matsjfunke
"""
import os
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, Form, HTTPException, Request, status, Query
from fastapi.responses import HTMLResponse, JSONResponse

from starlette.responses import RedirectResponse
from starlette.status import HTTP_308_PERMANENT_REDIRECT

from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

# importing authentication functions from authentication.py
from .authentication import authenticate_user, create_access_token, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, json_db

# uncomment this to enable enpoint /create-password which hashes password
# from .password_encryption import router as password_router
# add app.include_router(password_router) in line after app = FastAPI()

app = FastAPI()

# Initialize template directory relative to the current file location
current_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    print("get login")
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), time_frame: str = Form(...)):
    print("login post")
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
    redirect_url = f"/hello?time_frame={time_frame}"

    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_308_PERMANENT_REDIRECT)
    response.set_cookie(key="access_token", value=access_token)

    print("Response content before returning: ", response)
    print("Redirect URL:", response.headers["location"])
    print("Status Code:", response.status_code)
    return response


@app.post("/hello")
def hello(request: Request, time_frame: str = Query(...)):
    access_token = request.cookies.get("access_token")
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no cookies, in your jar",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print("access_token", access_token)

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"hello": "world", "time_frame": time_frame, "access_token": access_token}
