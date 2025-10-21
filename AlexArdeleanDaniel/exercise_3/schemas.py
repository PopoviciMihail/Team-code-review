from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=0, le=datetime.now().year)
    isbn: str = Field(..., min_length=10, max_length=13)

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=0, le=datetime.now().year)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    isbn: str
