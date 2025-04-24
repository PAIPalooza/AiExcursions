"""
Supabase client configuration and initialization.
"""
from typing import Optional
from supabase import create_client, Client
from .config import get_settings

_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """
    Get or create a Supabase client instance.
    Uses singleton pattern to avoid multiple client instances.
    
    Returns:
        Client: Initialized Supabase client
        
    Raises:
        Exception: If client initialization fails
    """
    global _supabase_client
    
    if _supabase_client is None:
        try:
            settings = get_settings()
            _supabase_client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
        except Exception as e:
            raise Exception(f"Failed to initialize Supabase client: {str(e)}")
    
    return _supabase_client


def reset_supabase_client() -> None:
    """Reset the Supabase client singleton for testing purposes."""
    global _supabase_client
    _supabase_client = None
