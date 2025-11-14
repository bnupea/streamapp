from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from functools import lru_cache
import os

load_dotenv()


@lru_cache()
def get_client() -> AsyncIOMotorClient:
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError(
            "MONGO_URI environment variable is not set. "
            "Please set it in your environment or .env file."
        )
    
    # Connection options for production deployments
    # These help with connection stability and timeout handling
    connection_options = {
        "serverSelectionTimeoutMS": 5000,  # 5 seconds timeout for server selection
        "connectTimeoutMS": 10000,  # 10 seconds connection timeout
        "socketTimeoutMS": 20000,  # 20 seconds socket timeout
        "retryWrites": True,  # Enable retryable writes
        "retryReads": True,  # Enable retryable reads
        "maxPoolSize": 50,  # Maximum number of connections in the pool
        "minPoolSize": 10,  # Minimum number of connections in the pool
    }
    
    return AsyncIOMotorClient(mongo_uri, **connection_options)


def get_database() -> AsyncIOMotorDatabase:
    client = get_client()
    db_name = os.getenv("DB_NAME", "assignmentdb")
    return client[db_name]

