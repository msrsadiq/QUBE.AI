"""
Configuration module for Qube.AI application.
Loads environment variables and provides centralized configuration management.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


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
        DATABASE_URL: Database connection string
        CORS_ORIGINS: List of allowed CORS origins
        ADMIN_USERNAME: Default admin username for initial setup
        ADMIN_PASSWORD: Default admin password for initial setup
        LOG_LEVEL: Logging level (INFO, DEBUG, WARNING, ERROR)
        BACKEND_CORS_ORIGINS: Backend CORS origins (JSON string)
        OLLAMA_BASE_URL: Ollama API base URL for LLM integration
        MAX_FILE_SIZE: Maximum file upload size in bytes
        ALLOWED_FILE_TYPES: Allowed file extensions for uploads
    
    Note:
        Pydantic 2.x forbids extra fields by default. All env vars must be declared here.
    """
    
    # Application Configuration
    APP_NAME: str = "Qube.AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Security Configuration
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./qubeai.db"
    
    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    BACKEND_CORS_ORIGINS: str = '["http://localhost:3000","http://127.0.0.1:3000"]'
    
    # Admin User Configuration
    ADMIN_USERNAME: str = "Admin"
    ADMIN_PASSWORD: str = "Admin"
    
    # LLM Configuration (Future use)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # File Upload Configuration (Future use)
    MAX_FILE_SIZE: int = 10485760  # 10MB in bytes
    ALLOWED_FILE_TYPES: str = '[".txt", ".pdf", ".docx", ".xlsx", ".csv", ".json"]'
    
    # Pydantic V2 Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Allow extra fields in .env without validation errors
    )
    
    def get_cors_origins(self) -> List[str]:
        """
        Parse CORS origins from comma-separated string to list.
        
        Returns:
            List[str]: List of allowed CORS origin URLs
        """
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()