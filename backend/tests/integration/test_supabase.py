"""
Integration tests for Supabase client functionality.
"""
import pytest
from unittest.mock import patch
from supabase import Client, create_client
from postgrest import APIError

from app.core.supabase import get_supabase_client, reset_supabase_client
from app.core.config import get_settings

settings = get_settings()


@pytest.fixture(autouse=True)
def cleanup_supabase_client():
    """Reset Supabase client after each test."""
    yield
    reset_supabase_client()


@pytest.fixture
def mock_supabase_client():
    """Create a mock Supabase client."""
    with patch("supabase.create_client") as mock_create:
        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        mock_create.return_value = client
        yield client


def test_supabase_client_initialization(mock_supabase_client):
    """
    Given: The Supabase configuration
    When: Initializing a Supabase client
    Then: It should return a valid client instance
    """
    client = get_supabase_client()
    assert isinstance(client, Client)
    assert client.supabase_url == settings.SUPABASE_URL
    assert client.supabase_key == settings.SUPABASE_KEY


@pytest.mark.asyncio
async def test_supabase_auth_flow():
    """
    Given: A Supabase client
    When: Performing authentication operations
    Then: It should handle the auth flow correctly
    """
    client = get_supabase_client()
    
    # Test sign up with invalid credentials
    with pytest.raises(Exception) as exc_info:
        await client.auth.sign_up({
            "email": "test@example.com",
            "password": "test"  # Too short password
        })
    assert "Password should be at least 6 characters" in str(exc_info.value)


@pytest.mark.asyncio
async def test_supabase_data_operations():
    """
    Given: A Supabase client
    When: Performing database operations
    Then: It should handle data operations correctly
    """
    client = get_supabase_client()
    
    # Test data fetch from non-existent table
    with pytest.raises(APIError) as exc_info:
        await client.table("nonexistent_table").select("*").execute()
    assert "does not exist" in str(exc_info.value)


def test_supabase_client_auth():
    """
    Given: A Supabase client
    When: Checking client configuration
    Then: It should have auth client configured
    """
    client = get_supabase_client()
    assert client.auth is not None
    assert client.auth._url == f"{settings.SUPABASE_URL}/auth/v1"
    assert "Authorization" in client.auth._headers
