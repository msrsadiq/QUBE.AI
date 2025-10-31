from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserLogin(BaseModel):
    """Login request schema"""
    username: str
    password: str

class UserCreate(BaseModel):
    """User registration schema"""
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: str
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str
    user: dict  # Contains user info

class TokenData(BaseModel):
    """Token data schema"""
    username: Optional[str] = None