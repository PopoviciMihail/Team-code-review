from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

from Model.book import Book
from Model.user import User

class UserBookBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="book.id")
    added_date: datetime = Field(default_factory=datetime.utcnow)
    
class UserBook(UserBookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)