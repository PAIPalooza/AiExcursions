import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from jose import jwt
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.config import settings
from app.db.base_class import Base
from app.api import deps

# Override the database URL for testing
settings.SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create async test database engine
test_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create async session factory
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Override the get_db dependency
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[deps.get_db] = override_get_db

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest_asyncio.fixture
async def async_client():
    """Create an async test client."""
    async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as client:
        yield client

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
def auth_headers(valid_token):
    """Create authorization headers with valid token."""
    return {"Authorization": f"Bearer {valid_token}"}

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

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """Set up test database before each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
