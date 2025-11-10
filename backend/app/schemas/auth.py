"""
Authentication Schemas
---------------------
Pydantic models for authentication request/response validation.

These schemas handle:
- Login request validation
- JWT token response formatting
- User profile data serialization
"""

from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    """
    Schema for login request payload.
    
    Attributes:
        username: User's username
        password: User's password (plain text, will be hashed for comparison)
    """
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)
    
    class Config:
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
        access_token: JWT token for authentication
        token_type: Token type (always "bearer")
        username: Authenticated user's username
    """
    access_token: str
    token_type: str
    username: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "username": "Admin"
            }
        }


class UserResponse(BaseModel):
    """
    Schema for user profile information.
    
    Attributes:
        id: User's unique identifier
        username: User's username
        email: User's email (optional)
        is_active: Whether user account is active
        is_admin: Whether user has admin privileges
    """
    id: int
    username: str
    email: Optional[str] = None
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "Admin",
                "email": "admin@qubeai.com",
                "is_active": True,
                "is_admin": True
            }
        }