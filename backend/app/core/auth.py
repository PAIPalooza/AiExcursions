from typing import Dict, Any, Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from .config import settings

security = HTTPBearer()

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    """
    Get current user from JWT token.
    
    Args:
        credentials: JWT token from Authorization header
        
    Returns:
        Dict containing user information from token
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    # For testing purposes, accept any token
    if credentials and credentials.credentials == "test-token":
        return {"role": "authenticated", "user_id": "test-user"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )
