from pydantic_settings import BaseSettings
from typing import List
import secrets


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Qube.AI"
    DEBUG: bool = True
    
    # Database Configuration
    DATABASE_URL: str
    
    # Security Configuration
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()