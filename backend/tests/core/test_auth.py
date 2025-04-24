"""
Unit tests for authentication functionality.
"""
import pytest
from fastapi import HTTPException, security
from jose import jwt
from unittest.mock import AsyncMock, MagicMock

from app.core.auth import get_current_user
from app.core.config import get_settings

settings = get_settings()


@pytest.mark.asyncio
async def test_get_current_user_missing_token():
    """
    Given: No authentication token
    When: Validating user credentials
    Then: It should raise an HTTPException
    """
    mock_credentials = MagicMock()
    mock_credentials.credentials = None
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(mock_credentials)
    assert exc_info.value.status_code == 401
    assert "Not authenticated" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_get_current_user_invalid_signature():
    """
    Given: A token signed with wrong secret
    When: Validating user credentials
    Then: It should raise an HTTPException
    """
    wrong_token = jwt.encode(
        {
            "sub": "test-user",
            "role": "authenticated",
            "exp": 2000000000
        },
        "wrong_secret",
        algorithm="HS256"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(type("Credentials", (), {"credentials": wrong_token})())
    assert exc_info.value.status_code == 401
    assert "Invalid authentication token" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_get_current_user_missing_claims():
    """
    Given: A token missing required claims
    When: Validating user credentials
    Then: It should raise an HTTPException
    """
    incomplete_token = jwt.encode(
        {
            "exp": 2000000000
        },
        settings.SUPABASE_JWT_SECRET,
        algorithm="HS256"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(type("Credentials", (), {"credentials": incomplete_token})())
    assert exc_info.value.status_code == 401
    assert "Invalid user ID in token" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_get_current_user_malformed_token():
    """
    Given: A malformed token
    When: Validating user credentials
    Then: It should raise an HTTPException
    """
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(type("Credentials", (), {"credentials": "not.a.token"})())
    assert exc_info.value.status_code == 401
    assert "Invalid authentication token" in str(exc_info.value.detail)
