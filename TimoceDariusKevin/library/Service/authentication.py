from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import select
from jose import JWTError, jwt
from Database.SqlEngine import SessionDependency
from Model.user import User

SECRET_KEY = "Whatever currently"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password) -> bool:
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    # Truncate the string to ensure UTF-8 encoding won't exceed 72 bytes
    # We'll find the maximum number of characters that fit in 72 bytes
    encoded = password.encode('utf-8')
    print(password)
    print(len(encoded))
    if len(encoded) > 72:
        # Truncate bytes and decode back to string
        truncated_bytes = encoded[:72]
        # Remove any incomplete multi-byte characters at the end
        while truncated_bytes[-1] & 0b11000000 == 0b10000000:
            truncated_bytes = truncated_bytes[:-1]
        password = truncated_bytes.decode('utf-8', 'ignore')
    return password_context.hash(password)

def authenticate_user(session: SessionDependency, username: str, password: str):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = str(payload.get("sub"))
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

async def require_admin(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def require_privileged(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role not in ["Admin", "Privileged"]:
        raise HTTPException(status_code=403, detail="Privileged access required")
    return current_user