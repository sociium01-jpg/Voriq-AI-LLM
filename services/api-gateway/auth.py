import os
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

SECRET_KEY = os.getenv("JWT_SECRET", "vorik_ai_jwt_super_secret_key_change_in_production_32bytes")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

class TokenData(BaseModel):
    user_id: str
    email: str
    role: str
    organisation_id: Optional[str] = None

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')[:72]  # Truncate to max 72 bytes for bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role", "member")
        organisation_id: str = payload.get("organisation_id")
        if user_id is None or email is None:
            raise credentials_exception
        return TokenData(user_id=user_id, email=email, role=role, organisation_id=organisation_id)
    except jwt.PyJWTError:
        raise credentials_exception

async def get_optional_user(token: Optional[str] = Depends(oauth2_scheme)) -> TokenData:
    if not token or token in ["demo-token", "null", "undefined", "bearer demo-token"]:
        return TokenData(user_id="guest_user", email="guest@voriq.ai", role="member", organisation_id="default_org")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub", "guest_user")
        email: str = payload.get("email", "guest@voriq.ai")
        role: str = payload.get("role", "member")
        organisation_id: str = payload.get("organisation_id", "default_org")
        return TokenData(user_id=user_id, email=email, role=role, organisation_id=organisation_id)
    except Exception:
        return TokenData(user_id="guest_user", email="guest@voriq.ai", role="member", organisation_id="default_org")

def require_role(allowed_roles: list[str]):
    async def role_checker(current_user: TokenData = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{current_user.role}' lacks permission. Required: {allowed_roles}"
            )
        return current_user
    return role_checker
