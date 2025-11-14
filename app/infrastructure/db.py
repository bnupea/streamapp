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
    # Check for MONGO_URI first (preferred), then fall back to MONGO_URL
    mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGO_URL")
    
    # Debug: Log available environment variables (without sensitive values)
    if not mongo_uri:
        logger.warning("MONGO_URI/MONGO_URL not found in environment variables")
        # List all env vars that start with MONGO or DB for debugging
        relevant_vars = {k: "***" if "PASSWORD" in k.upper() or "SECRET" in k.upper() or "URI" in k.upper() or "URL" in k.upper() else v 
                        for k, v in os.environ.items() 
                        if "MONGO" in k.upper() or "DB" in k.upper()}
        logger.info(f"Relevant environment variables found: {list(relevant_vars.keys())}")
    
    if not mongo_uri:
        # Provide helpful error message for deployment
        error_msg = (
            "MONGO_URI or MONGO_URL environment variable is not set.\n"
            "For deployment, set it in your platform's environment variables:\n"
            "  - Render: Add in Environment tab\n"
            "  - Heroku: Use 'heroku config:set MONGO_URI=...'\n"
            "  - Docker: Set in docker-compose.yml or -e flag\n"
            "  - Other: Set in your platform's environment variable settings\n"
            "\n"
            "Example: mongodb+srv://user:password@cluster.mongodb.net/"
        )
        raise ValueError(error_msg)
    
    # Log which variable was used (but don't log the actual value for security)
    if os.getenv("MONGO_URI"):
        logger.info("MONGO_URI found in environment variables")
    elif os.getenv("MONGO_URL"):
        logger.info("MONGO_URL found in environment variables (using as MONGO_URI)")
    
    # Connection options for production deployments
    # For mongodb+srv:// connections, TLS is automatically enabled by MongoDB Atlas
    # We don't need to explicitly set tls=True for +srv connections
    connection_options = {
        "serverSelectionTimeoutMS": 30000,  # 30 seconds (increased for SSL handshake)
        "connectTimeoutMS": 30000,  # 30 seconds (increased for SSL handshake)
        "socketTimeoutMS": 30000,  # 30 seconds socket timeout
        "retryWrites": True,  # Enable retryable writes
        "retryReads": True,  # Enable retryable reads
        "maxPoolSize": 50,  # Maximum number of connections in the pool
        "minPoolSize": 10,  # Minimum number of connections in the pool
    }
    
    # For mongodb+srv://, TLS is automatically enabled - don't set it explicitly
    # Only set TLS options if NOT using +srv protocol
    if not mongo_uri.startswith("mongodb+srv://"):
        connection_options["tls"] = True
        connection_options["tlsAllowInvalidCertificates"] = False
        connection_options["tlsAllowInvalidHostnames"] = False
    
    return AsyncIOMotorClient(mongo_uri, **connection_options)


def get_database() -> AsyncIOMotorDatabase:
    client = get_client()
    db_name = os.getenv("DB_NAME", "assignmentdb")
    return client[db_name]

