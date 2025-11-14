from typing import Dict
from app.domain.user import User, UserRepository

class InMemoryUserRepo(UserRepository):
    def __init__(self):
        self._store: Dict[str, User] = {}

    async def get_by_email(self, email: str) -> User | None:
        return self._store.get(email)

    async def add(self, user: User) -> None:
        self._store[user.email] = user

