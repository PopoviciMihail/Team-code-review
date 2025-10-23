from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from Model.user import User, UserCreate, UserPublic, UserUpdate
from Service.authentication import require_admin, get_password_hash
from Database.SqlEngine import SessionDependency

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_router.post("/", response_model=UserPublic)
async def create_user(user: UserCreate, session: SessionDependency):
    # Hash password before storing
    hashed_password = get_password_hash(user.password)
    database_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    session.add(database_user)
    session.commit()
    session.refresh(database_user)
    return UserPublic(**database_user.model_dump())

@user_router.get("/", response_model=list[UserPublic])
async def read_users(
    current_user: Annotated[User, Depends(require_admin)],
    session: SessionDependency,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    """Get all users - Admin only"""
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return [UserPublic(**user.model_dump()) for user in users]

@user_router.get("/{user_id}", response_model=UserPublic)
async def read_user(
    current_user: Annotated[User, Depends(require_admin)],
    session: SessionDependency,
    user_id: int
):
    """Get user by ID - Admin only"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPublic(**user.model_dump())

@user_router.delete("/{user_id}")
async def delete_user(
    current_user: Annotated[User, Depends(require_admin)],
    session: SessionDependency,
    user_id: int
):
    """Delete user - Admin only"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

@user_router.patch("/{user_id}", response_model=UserPublic)
async def update_user(
    current_user: Annotated[User, Depends(require_admin)],
    session: SessionDependency,
    user_id: int, 
    user_update: UserUpdate
):
    """Update user - Admin only"""
    database_user = session.get(User, user_id)
    if not database_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(database_user, field, value)
    
    session.add(database_user)
    session.commit()
    session.refresh(database_user)
    return UserPublic(**database_user.model_dump())