from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Dict
"""
Exercise 3

Review the FastAPI tutorial (https://fastapi.tiangolo.com/tutorial/) carefully and use it to build a simple REST API for managing a collection of books in a library.

Endpoints requirements.
- Create a book
    Endpoint: POST /books/
    Request body:
    {
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "year": 1999,
        "isbn": "978-0201616224"
    }
    Response: Return the created book with a unique ID.
- Read all books
    Endpoint: GET /books/
    Response: List all stored books.
- Read a single book by ID
    Endpoint: GET /books/{book_id}
    Response: Return the book with that ID or an error if not found.
- Update a book
    Endpoint: PUT /books/{book_id}
    Request body: Same as creation.
    Response: Return the updated book.
- Delete a book
    Endpoint: DELETE /books/{book_id}
    Response: Confirm deletion.

Moreover, find a way to integrate the requests and pandas libraries into your solution. Use your creativity.
"""

app = FastAPI()

_DB={}
class Book(BaseModel):
    title: str
    author: str
    year: int
    isbn: str
    id: int
    
class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    isbn: str
    
@app.post("/books")
async def create_book(book:BookCreate):
    id = len(_DB)
    new_book = Book(
        id=id,
        title=book.title,
        author=book.author,
        year= book.year,
        isbn= book.isbn
    )
    _DB[id]=new_book
    return new_book

@app.get("/books")
async def list_books():
    return list(_DB.values())

@app.get("/books/{book_id}")
async def get_book(book_id:int):
    if book_id in _DB:
        return _DB[book_id]
    else:
        raise HTTPException(status_code=404,detail="Book not found")
    
@app.put("/books/{book_id}")
async def update_book(book_id:int,book:BookCreate):
    exists = await get_book(book_id)
    updated_book = Book(
        id=book_id,
        title=book.title,
        author=book.author,
        year= book.year,
        isbn= book.isbn
    )
    _DB[book_id]=updated_book
    return updated_book
    
@app.delete("/books/")
async def delete_book(book_id:int):
    exists = await get_book(book_id)
    _DB.pop(book_id)
    return {"message":"Book deleted succesfully" }
