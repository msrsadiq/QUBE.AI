"""
Authentication API endpoints.
Handles user login, logout, and current user information retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import verify_password, create_access_token
from ..core.dependencies import get_current_active_user
from ..models.user import User
from ..schemas.auth import LoginRequest, LoginResponse, UserResponse


# Router for authentication endpoints
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and generate access token.
    
    Args:
        credentials: Login credentials (username and password)
        db: Database session
        
    Returns:
        LoginResponse: Access token and user information
        
    Raises:
        HTTPException 401: If credentials are invalid
        
    Flow:
        1. Fetch user by username from database
        2. Verify password against stored hash
        3. Generate JWT token with user data
        4. Return token and user profile
        
    Security:
        - Password is verified using bcrypt
        - Token expires after configured time (default: 30 minutes)
        - Failed attempts are not rate-limited (future enhancement)
    """
    
    # Fetch user from database
    user = db.query(User).filter(User.username == credentials.username).first()
    
    # Validate user exists and password is correct
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Generate JWT access token
    access_token = create_access_token(data={"sub": user.username})
    
    # Return authentication response
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=user.username,
        full_name=user.full_name
    )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user)
):
    """
    Logout current user.
    
    Args:
        current_user: Currently authenticated user
        
    Returns:
        dict: Success message
        
    Note:
        JWT tokens are stateless, so actual logout is handled client-side
        by removing the token. This endpoint is provided for consistency
        and future server-side token blacklisting implementation.
        
    Future Enhancement:
        - Implement token blacklist/revocation
        - Track active sessions
        - Force logout from all devices
    """
    
    return {
        "message": "Successfully logged out",
        "username": current_user.username
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current authenticated user's profile information.
    
    Args:
        current_user: Currently authenticated user from token
        
    Returns:
        UserResponse: User profile data
        
    Usage:
        Used by frontend to verify token validity and display user info
        in the UI (e.g., username in header, user profile page)
    """
    
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active
    )