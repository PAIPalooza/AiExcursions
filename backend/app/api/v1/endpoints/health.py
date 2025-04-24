from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.get("")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/db")
async def health_check_db(db: AsyncSession = Depends(deps.get_db)):
    """Health check with database connection test."""
    try:
        # Try a simple database query
        await db.execute(text("SELECT 1"))
        await db.commit()
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database health check failed: {str(e)}"
        )
