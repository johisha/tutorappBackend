from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from typing import Optional


from passlib.context import CryptContext

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def verify_password(password: str, hashed: str) -> bool:
    return password_context.verify(password, hashed)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def create_access_token(data: dict, role: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "role": role})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception:
        return {}