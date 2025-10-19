from pydantic import BaseModel

class BookRequest(BaseModel):
    title: str
    author: str
    year: int
    isbn: str