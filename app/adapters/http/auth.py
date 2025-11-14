from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.usecase.auth_service import AuthService
from app.di import get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

class SignupIn(BaseModel):
    email: str
    password: str

class LoginIn(BaseModel):
    email: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/signup", response_model=TokenOut)
async def signup(payload: SignupIn, auth: AuthService = Depends(get_auth_service)):
    token = await auth.signup(payload.email, payload.password)
    return TokenOut(access_token=token)

@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn, auth: AuthService = Depends(get_auth_service)):
    token = await auth.login(payload.email, payload.password)
    return TokenOut(access_token=token)