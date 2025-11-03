"""
Pydantic schemas for authentication requests and responses.
Provides data validation and serialization for auth endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    """
    Schema for user login request.
    
    Attributes:
        username: User's login username
        password: User's plain password (transmitted over HTTPS)
        
    Validation:
        - Username: 3-50 characters
        - Password: 3-100 characters (minimum length for security)
    """
    
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username for authentication"
    )
    password: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Password for authentication"
    )
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "username": "Admin",
                "password": "Admin"
            }
        }


class LoginResponse(BaseModel):
    """
    Schema for successful login response.
    
    Attributes:
        access_token: JWT token for authenticated requests
        token_type: Type of token (always "bearer")
        username: Authenticated user's username
        full_name: User's display name (if available)
        
    Usage:
        Client should store access_token and include it in subsequent requests:
        Authorization: Bearer <access_token>
    """
    
    access_token: str = Field(
        ...,
        description="JWT access token for authentication"
    )
    token_type: str = Field(
        default="bearer",
        description="Token type (always 'bearer')"
    )
    username: str = Field(
        ...,
        description="Authenticated username"
    )
    full_name: Optional[str] = Field(
        None,
        description="User's full display name"
    )
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "username": "Admin",
                "full_name": "System Administrator"
            }
        }


class UserResponse(BaseModel):
    """
    Schema for user profile information.
    
    Attributes:
        id: User's unique identifier
        username: User's login username
        full_name: User's display name
        is_active: Whether user account is active
        
    Note:
        Excludes sensitive information like hashed_password
    """
    
    id: int
    username: str
    full_name: Optional[str] = None
    is_active: bool
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "Admin",
                "full_name": "System Administrator",
                "is_active": True
            }
        }