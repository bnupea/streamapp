from abc import ABC, abstractmethod
from typing import Protocol

from pydantic.v1 import BaseModel


class User(BaseModel):
    email: str
    password_hash: str


class UserRepository(Protocol):
    async def get_by_email(self, email: str) -> User | None: ...
    async def add(self, user: User) -> None: ...
