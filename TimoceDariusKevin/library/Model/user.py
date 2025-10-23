from enum import Enum
from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional

class RoleType(str, Enum):
    Admin = "Admin"
    Privileged = "Privileged"
    Guest = "Guest"

class UserBase(SQLModel):
    username: str = Field(index=True, min_length=3, max_length=50)
    email: EmailStr = Field(index=True)
    role: RoleType = Field(default=RoleType.Guest)

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str

class UserPublic(UserBase):
    id: int

class UserCreate(SQLModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    role: RoleType = Field(default=RoleType.Guest)

class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[RoleType] = None

class UserLogin(SQLModel):
    username: str
    password: str