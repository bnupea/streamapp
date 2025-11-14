import os

from fastapi import FastAPI, Depends, HTTPException, status
from app.adapters.http import stream_router, auth
from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastructure.db import get_client

app = FastAPI()

app.include_router(stream_router.router)
app.include_router(auth.router)



@app.get("/health/db", tags=["health"])
async def health_db(
    client: AsyncIOMotorClient = Depends(get_client)
):

    db_name = os.getenv("DB_NAME", "assignmentdb")
    try:
        await client[db_name].command("ping")
        return {
            "status": "ok",
            "mongo": "connected",
            "database": db_name,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MongoDB unreachable: {str(exc)}"
        )
