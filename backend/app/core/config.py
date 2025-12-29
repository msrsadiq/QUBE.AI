"""
Configuration module for Qube.AI application.
Loads environment variables and provides centralized configuration management.

UPDATED: Added support for extra fields and previous phase configurations.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        APP_NAME: Application name displayed in API docs
        APP_VERSION: Current version of the application
        DEBUG: Debug mode flag
        SECRET_KEY: Secret key for JWT token generation
        ALGORITHM: Algorithm used for JWT encoding/decoding
        ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time in minutes
        ENCRYPTION_KEY: Encryption key for API key storage
        DATABASE_URL: Database connection string
        CORS_ORIGINS: Allowed CORS origins (comma-separated)
        ADMIN_USERNAME: Default admin username for initial setup
        ADMIN_PASSWORD: Default admin password for initial setup
        DEFAULT_LLM_PROVIDER: Default LLM provider
        DEFAULT_LLM_MODEL: Default LLM model name
        DEFAULT_LLM_ENDPOINT: Default LLM API endpoint
    """
    
    # Application Configuration
    APP_NAME: str = "Qube.AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Security Configuration
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Encryption key for API keys (generate with: Fernet.generate_key())
    ENCRYPTION_KEY: str = "your-encryption-key-here-change-in-production"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./qubeai.db"
    
    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Admin User Configuration
    ADMIN_USERNAME: str = "Admin"
    ADMIN_PASSWORD: str = "Admin"
    
    # LLM Configuration
    DEFAULT_LLM_PROVIDER: str = "ollama"
    DEFAULT_LLM_MODEL: str = "llama3.1:8b"
    DEFAULT_LLM_ENDPOINT: str = "http://localhost:11434"
    
    # Optional fields from previous phases (will be ignored if not in .env)
    LOG_LEVEL: Optional[str] = "INFO"
    BACKEND_CORS_ORIGINS: Optional[str] = None
    MAX_FILE_SIZE: Optional[int] = None
    ALLOWED_FILE_TYPES: Optional[str] = None
    OLLAMA_BASE_URL: Optional[str] = None
    
    # Pydantic configuration - allow extra fields to be ignored
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'  # Ignore extra fields in .env that aren't defined here
    )


settings = Settings()