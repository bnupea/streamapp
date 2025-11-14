from fastapi import Depends

from app.adapters.repo.in_memory import InMemoryUserRepo
from app.adapters.repo.mongo_stream_repository import MongoStreamRepository
from app.infrastructure.db import get_database
from app.usecase.auth_service import AuthService
from app.usecase.stream_service import StreamService

def get_user_repo() -> InMemoryUserRepo:
    return InMemoryUserRepo()

def get_stream_service() -> StreamService:
    db = get_database()
    repo = MongoStreamRepository(db)
    return StreamService(repo)

def get_auth_service(user_repo=Depends(get_user_repo)) -> AuthService:
    user_repo = get_user_repo()
    return AuthService(user_repo)
