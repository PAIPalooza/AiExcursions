from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from pydantic import BaseModel

from ....core.auth import get_current_user

router = APIRouter()


class UserProfile(BaseModel):
    id: str
    email: str | None = None
    role: str | None = None


@router.get("/me", response_model=UserProfile)
async def read_user_me(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> UserProfile:
    """Get current user profile."""
    return UserProfile(
        id=current_user.get("sub", ""),
        email=current_user.get("email", ""),
        role=current_user.get("role", "")
    )
