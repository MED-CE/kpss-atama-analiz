from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import logging

from core.config import settings
from database.database import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from api.router import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["System"])
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint for Azure App Service / Functions ping.
    Checks database connectivity.
    """
    try:
        # Check DB connection
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "error"
        
    status = "ok" if db_status == "ok" else "degraded"
    
    return {
        "status": status,
        "database": db_status,
        "version": settings.VERSION
    }

@app.get("/", tags=["System"])
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
