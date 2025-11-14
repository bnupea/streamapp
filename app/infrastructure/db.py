from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from functools import lru_cache
import os
import logging

# Load .env file if it exists (for local development)
# In production/deployment, environment variables should be set directly
load_dotenv(override=False)

logger = logging.getLogger(__name__)


@lru_cache()
def get_client() -> AsyncIOMotorClient:
    mongo_uri = os.getenv("MONGO_URI")
    
    # Debug: Log available environment variables (without sensitive values)
    if not mongo_uri:
        logger.warning("MONGO_URI not found in environment variables")
        # List all env vars that start with MONGO or DB for debugging
        relevant_vars = {k: "***" if "PASSWORD" in k.upper() or "SECRET" in k.upper() or "URI" in k.upper() else v 
                        for k, v in os.environ.items() 
                        if "MONGO" in k.upper() or "DB" in k.upper()}
        logger.info(f"Relevant environment variables found: {list(relevant_vars.keys())}")
    
    if not mongo_uri:
        # Provide helpful error message for deployment
        error_msg = (
            "MONGO_URI environment variable is not set.\n"
            "For deployment, set it in your platform's environment variables:\n"
            "  - Render: Add in Environment tab\n"
            "  - Heroku: Use 'heroku config:set MONGO_URI=...'\n"
            "  - Docker: Set in docker-compose.yml or -e flag\n"
            "  - Other: Set in your platform's environment variable settings\n"
            "\n"
            "Example: mongodb+srv://user:password@cluster.mongodb.net/"
        )
        raise ValueError(error_msg)
    
    # Log that we found the URI (but don't log the actual value for security)
    logger.info("MONGO_URI found in environment variables")
    
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

