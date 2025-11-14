import os
import logging

from fastapi import FastAPI, Depends, HTTPException, status
from app.adapters.http import stream_router, auth
from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastructure.db import get_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(stream_router.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup_db_client():
    """Verify MongoDB connection on startup"""
    try:
        client = get_client()
        db_name = os.getenv("DB_NAME", "assignmentdb")
        # Test the connection
        await client[db_name].command("ping")
        logger.info(f"✅ Successfully connected to MongoDB database: {db_name}")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
        logger.error("Please check your MONGO_URI and DB_NAME environment variables")
        # Don't raise here - let the app start and handle errors in health check
        # This allows the container to start even if DB is temporarily unavailable



@app.get("/health/env", tags=["health"])
async def health_env():
    """Check environment variables (for debugging)"""
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME", "assignmentdb")
    
    return {
        "MONGO_URI_set": bool(mongo_uri),
        "MONGO_URI_length": len(mongo_uri) if mongo_uri else 0,
        "MONGO_URI_preview": f"{mongo_uri[:20]}..." if mongo_uri and len(mongo_uri) > 20 else (mongo_uri if mongo_uri else "NOT SET"),
        "DB_NAME": db_name,
        "all_env_vars_with_mongo": [k for k in os.environ.keys() if "MONGO" in k.upper() or "DB" in k.upper()],
    }


@app.get("/health/db", tags=["health"])
async def health_db(
    client: AsyncIOMotorClient = Depends(get_client)
):
    """Health check endpoint for MongoDB connection"""
    db_name = os.getenv("DB_NAME", "assignmentdb")
    mongo_uri = os.getenv("MONGO_URI", "not set")
    
    try:
        # Test connection with ping command
        await client[db_name].command("ping")
        return {
            "status": "ok",
            "mongo": "connected",
            "database": db_name,
            "uri_set": bool(mongo_uri and mongo_uri != "not set"),
        }
    except ValueError as exc:
        # This catches missing environment variable errors
        logger.error(f"Configuration error: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MongoDB configuration error: {str(exc)}"
        )
    except Exception as exc:
        # This catches connection errors
        logger.error(f"MongoDB connection error: {str(exc)}")
        error_type = type(exc).__name__
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MongoDB unreachable ({error_type}): {str(exc)}"
        )
