from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from Model.user import User, UserCreate
from Service.authentication import (
    authenticate_user, create_access_token, get_password_hash, 
    ACCESS_TOKEN_EXPIRE_MINUTES, SessionDependency
)
from sqlmodel import select

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post("/register")
async def register(user: UserCreate, session: SessionDependency):
    # Check if user exists
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    existing_email = session.exec(select(User).where(User.email == user.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return {"message": "User created successfully"}

@auth_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDependency):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }