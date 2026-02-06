"""
Supabase Client Singleton
Provides a single instance of Supabase client for the application
"""

from supabase import create_client, Client
from ..config import Config


class SupabaseClient:
    """Singleton class for Supabase client"""
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance
    
    def _initialize_client(self):
        """Initialize the Supabase client"""
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise ValueError(
                "Supabase configuration missing. "
                "Please set SUPABASE_URL and SUPABASE_KEY in your .env file"
            )
        
        self._client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        print(f"✅ Supabase client initialized: {Config.SUPABASE_URL[:30]}...")
    
    @property
    def client(self) -> Client:
        """Get the Supabase client instance"""
        return self._client


def get_supabase() -> Client:
    """
    Get Supabase client instance
    
    Returns:
        Supabase Client instance
    """
    return SupabaseClient().client
