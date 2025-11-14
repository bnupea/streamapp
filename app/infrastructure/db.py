from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from functools import lru_cache
import os

load_dotenv()


@lru_cache()
def get_client() -> AsyncIOMotorClient:
    mongo_uri = os.getenv("MONGO_URI")
    return AsyncIOMotorClient(mongo_uri)


def get_database() -> AsyncIOMotorDatabase:
    client = get_client()
    db_name = os.getenv("DB_NAME")
    return client[db_name]

