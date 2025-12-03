"""
Configuration module for Qube.AI application.
Loads environment variables and provides centralized configuration management.
"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
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
    
    class Config:
        """Pydantic configuration class."""
        env_file = ".env"
        case_sensitive = True


settings = Settings()