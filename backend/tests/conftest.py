import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app.main import app
from app.core.config import get_settings

settings = get_settings()


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def valid_token():
    """Create a valid JWT token for testing."""
    payload = {
        "sub": "test-user-id",
        "email": "test@example.com",
        "role": "authenticated",
        "exp": 2000000000,  # Far in the future
        "iat": 1600000000
    }
    return jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")


@pytest.fixture
def invalid_token():
    """Create an invalid JWT token for testing."""
    payload = {
        "sub": "test-user-id",
        "email": "test@example.com",
        # Missing required 'role' claim
        "exp": 2000000000,
        "iat": 1600000000
    }
    return jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")


@pytest.fixture
def expired_token():
    """Create an expired JWT token for testing."""
    payload = {
        "sub": "test-user-id",
        "email": "test@example.com",
        "role": "authenticated",
        "exp": 1600000000,  # In the past
        "iat": 1500000000
    }
    return jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")
