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

from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import requests
app = FastAPI()

class Book(BaseModel):
    """Represents a book with its key attributes."""
    title : str
    author: str
    year: int
    isbn: str
        
    def __str__(self):
        return f"The book with the title {self.title}, written by {self.author} was published in {self.year} and can be found by ID: {self.isbn}"

class MyException(Exception):
    """Custom exception for application-specific errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

book1 = Book(title="1984", author="George Orwell", year=1949, isbn="978-0451524935")
book2 = Book(title="To Kill a Mockingbird", author="Harper Lee", year=1960, isbn="978-0061120084")
book3 = Book(title="The Great Gatsby", author="F. Scott Fitzgerald", year=1925, isbn="978-0743273565")
book4 = Book(title="Pride and Prejudice", author="Jane Austen", year=1813, isbn="978-1503290563")
book5 = Book(title="The Catcher in the Rye", author="J.D. Salinger", year=1951, isbn="978-0316769488")

db = {
    "1": book1,
    "2": book2,
    "3": book3,
    "4": book4,
    "5": book5
}

@app.post("/books/")
async def create_book(new_book: Book, id: Optional[int]= None):
    """
    Create a new book entry in the in-memory database.
    If an ID already exists, raise a custom exception.
    """
    if str(id) in db:
            raise MyException("The book is already in the database")
    else:
            db[str(id)] = new_book
    return db[str(id)]
    
    
@app.get("/books/")
async def list_books():
    """List all books currently stored in the database."""
    return db


@app.get("/books/{book_id}")
async def list_single_book(book_id :str):
    """Retrieve a single book by its ID."""
    if book_id not in db:
        raise HTTPException(status_code= 400, detail="No book available with this ID to list")
    else:
        return db[book_id]
    
    
@app.put("/books/{book_id}")
async def update_book(book_id: str, new_book: Book):
    """Update the details of an existing book."""
    if book_id not in db:
        raise HTTPException(status_code= 400, detail="No book available with this ID to update")
    else:
        db[book_id] = new_book
        return db[book_id]
    
    
@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    """Delete a book by ID."""
    if book_id not in db:
        raise MyException("No book availabel to delete with this ID")
    else:
        del db[book_id]
        return {"message": "The deletion was done successfully"}

@app.get("/external-books/")
async def fetch_external_books(query: str = "python programming"):
    """
    Fetch books from the Google Books API.
    Only the first 5 results are returned for simplicity.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch external books")
    
    data = response.json()
    books = [
        {
            "title": item["volumeInfo"].get("title"),
            "authors": item["volumeInfo"].get("authors"),
            "publishedDate": item["volumeInfo"].get("publishedDate"),
        }
        for item in data.get("items", [])[:5]
    ]
    return {"query": query, "results": books}