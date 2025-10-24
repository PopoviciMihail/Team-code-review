from pydantic import BaseModel

class BookRequest(BaseModel):
    title: str
    author: str
    year: int
    isbn: str

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
    isbn: str
    
    class Config:
        from_attributes = True