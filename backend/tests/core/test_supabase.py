"""
Unit tests for Supabase client functionality.
"""
import pytest
from unittest.mock import patch, MagicMock
from supabase import Client

from app.core.supabase import get_supabase_client, reset_supabase_client
from app.core.config import get_settings

settings = get_settings()


@pytest.fixture(autouse=True)
def cleanup_supabase_client():
    """Reset Supabase client after each test."""
    yield
    reset_supabase_client()


def test_get_supabase_client_singleton():
    """
    Given: Multiple calls to get_supabase_client
    When: Getting the Supabase client
    Then: It should return the same instance
    """
    client1 = get_supabase_client()
    client2 = get_supabase_client()
    assert client1 is client2


def test_get_supabase_client_initialization_error():
    """
    Given: Invalid Supabase credentials
    When: Initializing the client
    Then: It should raise an exception with details
    """
    with patch("app.core.supabase.create_client") as mock_create:
        mock_create.side_effect = Exception("Network error")
        
        with pytest.raises(Exception) as exc_info:
            get_supabase_client()
        assert "Failed to initialize Supabase client" in str(exc_info.value)
        assert "Network error" in str(exc_info.value)


def test_reset_supabase_client():
    """
    Given: An existing Supabase client
    When: Resetting the client
    Then: It should create a new instance on next get
    """
    client1 = get_supabase_client()
    reset_supabase_client()
    client2 = get_supabase_client()
    assert client1 is not client2


@patch("app.core.supabase.create_client")
def test_supabase_client_configuration(mock_create):
    """
    Given: Valid Supabase credentials
    When: Creating a client
    Then: It should use the correct configuration
    """
    mock_client = MagicMock(spec=Client)
    mock_create.return_value = mock_client
    
    client = get_supabase_client()
    
    mock_create.assert_called_once_with(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY
    )
    assert client is mock_client
