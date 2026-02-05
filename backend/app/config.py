import os
from dotenv import load_dotenv

load_dotenv()  # load .env → environment variables

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLAlchemy connection pool settings to prevent connection timeouts
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before using them
        'pool_recycle': 300,    # Recycle connections after 5 minutes
        'pool_size': 10,        # Maximum number of connections
        'max_overflow': 20,     # Allow up to 20 additional connections
        'connect_args': {
            'connect_timeout': 10,  # Connection timeout in seconds
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5
        }
    }
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # JWT token configuration
    JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
    JWT_EXP_MINUTES = int(os.getenv("JWT_EXP_MINUTES", 1440))  # 24 hours default
    
    # Supabase configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "uploads")