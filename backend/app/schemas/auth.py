"""
Authentication Schemas
---------------------
Pydantic models for authentication requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    """
    Login request schema.
    
    Attributes:
        username: User's username
        password: User's password (plain text, will be verified)
    """
    username: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    """
    User information in responses.
    
    Attributes:
        id: User ID
        username: Username
        email: Email address (optional)
        is_admin: Admin flag
    """
    id: int
    username: str
    email: Optional[str] = None
    is_admin: bool = False
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """
    Login response schema.
    
    Attributes:
        access_token: JWT access token
        token_type: Token type (always "bearer")
        user: User information
    """
    access_token: str
    token_type: str = "bearer"
    user: UserResponse