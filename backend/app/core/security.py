from datetime import datetime, timedelta
from typing import Optional, Any
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)

def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: Token subject (usually username)
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def create_refresh_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        subject: Token subject (usually username)
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT refresh token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)  # 7 days for refresh token
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def decode_token(token: str) -> dict:
    """
    Decode a JWT token.
    
    Args:
        token: JWT token
        
    Returns:
        Decoded token payload
        
    Raises:
        JWTError: If token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise JWTError(f"Could not decode token: {str(e)}")

def is_token_expired(token: str) -> bool:
    """
    Check if a token is expired.
    
    Args:
        token: JWT token
        
    Returns:
        True if expired, False otherwise
    """
    try:
        payload = decode_token(token)
        exp = payload.get("exp")
        
        if not exp:
            return True
            
        return datetime.utcnow() > datetime.fromtimestamp(exp)
        
    except JWTError:
        return True

def encrypt_sensitive_data(data: str) -> str:
    """
    Encrypt sensitive data (placeholder - implement proper encryption).
    
    Args:
        data: Data to encrypt
        
    Returns:
        Encrypted data
        
    Note:
        In production, use proper encryption library like cryptography
    """
    # TODO: Implement proper encryption for sensitive data
    # For now, just return the data (NOT SECURE)
    return data

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """
    Decrypt sensitive data (placeholder - implement proper decryption).
    
    Args:
        encrypted_data: Encrypted data
        
    Returns:
        Decrypted data
        
    Note:
        In production, use proper encryption library like cryptography
    """
    # TODO: Implement proper decryption for sensitive data
    # For now, just return the data (NOT SECURE)
    return encrypted_data