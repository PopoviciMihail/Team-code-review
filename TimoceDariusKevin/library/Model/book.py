from pydantic import field_validator
from typing import Optional
from sqlmodel import SQLModel, Field as SQLField, Relationship
from typing import List

class BookBase(SQLModel):
    title: str = SQLField(..., min_length=1, max_length=200)
    author: str = SQLField(..., min_length=1, max_length=100)
    pseudonym: Optional[str] = SQLField(None, min_length=1, max_length=100)
    year: int = SQLField(..., ge=1000, le=2024)
    isbn: str = SQLField(..., min_length=10, max_length=20)
    quantity: int = SQLField(..., ge=0)

class Book(BookBase, table=True):
    id: int = SQLField(default=None, primary_key=True)
    
    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, field):
        if not any(prefix in field.lower() for prefix in ['isbn', '978', '979']):
            raise ValueError('ISBN should contain "isbn", "978", or "979"')
        return field

class BookPublic(BookBase):
    id: int
    author: str

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class PrivilegedBook(BookPublic):
    author_true: str