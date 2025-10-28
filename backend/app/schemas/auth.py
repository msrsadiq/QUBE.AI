from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    role: str
    
    class Config:
        from_attributes = True