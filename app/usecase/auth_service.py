from typing import Annotated
from fastapi import Depends, HTTPException, status

from app.domain.user import User, UserRepository
from app.infrastructure.security import (
    hash_password, verify_password, create_access_token, decode_token
)

class AuthService:
    def __init__(self, user_repo: Annotated[UserRepository, Depends()]):
        self.user_repo = user_repo

    async def signup(self, email: str, password: str) -> str:
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed = hash_password(password)
        await self.user_repo.add(User(email=email, password_hash=hashed))
        return create_access_token({"sub": email})

    async def login(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return create_access_token({"sub": email})

    @staticmethod
    def get_current_user(token: str) -> str:
        try:
            payload = decode_token(token)
            email: str | None = payload.get("sub")
            if email is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return email
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")