"""
Mats Funke
26.01.2024
"""
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from passlib.context import CryptContext

router = APIRouter()

@router.get("/create-password", response_class=HTMLResponse)
async def createpassword_from():
    return """
    <form action="/hashed-password" method="post">
        <input type="text" name="plain_password" placeholder="enter password">
        <input type="submit">
    </form>
    """

@router.post("/hashed-password")
async def hash_password(plain_password: str = Form(...)):
    """uses pwd_context to encrypt the plain_password from the /create-password html from"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(plain_password)
    return {"hashed_password": hashed_password}