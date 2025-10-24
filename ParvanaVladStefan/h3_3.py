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
from pydantic import BaseModel,Field, ValidationError
import pandas as pd
from typing import List, Annotated
import requests
from google import genai
from os import getenv


class Book(BaseModel):
    title: Annotated[str,Field(max_length=100, min_length=1, description="Title of the book", example="The Pragmatic Programmer")]
    author: Annotated[str,Field(max_length=100, min_length=1, description="Author of the book", example="Andrew Hunt")]
    year: Annotated[int,Field(gt=0, description="Publication year of the book", example=1999)]
    isbn: Annotated[str,Field(max_length=20, min_length=10, description="ISBN number of the book", example="978-0201616224")]
    summary: Annotated[str|None,Field(default=None, description="AI-generated summary of the book", example="A comprehensive guide to pragmatic programming techniques.")]=None


class BookEntity(Book):
    id: Annotated[int,Field(gt=0, description="Unique ID of the book", example=1,default_factory=lambda: ID_COUNTER)]

ID_COUNTER = 1 
BOOKS = list()
API_KEY = getenv("API_KEY")

client = genai.Client(api_key=API_KEY)

def generate_summary(book: BookEntity) -> str:
    """Generate summary only once for a given book."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=f"Provide a concise 2–3 sentence summary for the book '{book.title}' by {book.author}."
        )
        return response.text.strip()
    except Exception:
        return "Summary generation failed."
    
async def lifespan(app: FastAPI):
    global BOOKS, ID_COUNTER
    try:
        df = pd.read_csv("books_data.csv")
        BOOKS = []
        for _, row in df.iterrows():
            book = BookEntity(
                id=int(row['id']),
                title=row['title'],
                author=row['author'],
                year=int(row['year']),
                isbn=row['isbn']
            )
            BOOKS.append(book)
        ID_COUNTER = max(book.id for book in BOOKS) + 1 if BOOKS else 1
    except FileNotFoundError:
        BOOKS = []
        ID_COUNTER = 1

    yield 

    if BOOKS:
        df = pd.DataFrame([book.model_dump() for book in BOOKS])
        df = df[['id', 'title', 'author', 'year', 'isbn','summary']] 
        df.to_csv("books_data.csv", index=False)


app = FastAPI(lifespan=lifespan)

@app.post("/books/", response_model=BookEntity, status_code=201)
def create_book(book: Book):
    global ID_COUNTER
    new_book = BookEntity(id=ID_COUNTER, **book.model_dump())

    if not new_book.summary:
        new_book.summary = generate_summary(new_book)

    BOOKS.append(new_book)
    ID_COUNTER += 1
    return new_book


@app.get("/books/", response_model=List[BookEntity], status_code=200)
def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", response_model=BookEntity, status_code=200)
def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            if not book.summary or book.summary.strip() == "":
                book.summary = generate_summary(book)
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}", response_model=BookEntity, status_code=200)
def update_book(book_id: int, updated_book: Book):
    for index, existing_book in enumerate(BOOKS):
        if existing_book.id == book_id:
            if (
                existing_book.title != updated_book.title
                or existing_book.author != updated_book.author
            ):
                updated_book.summary = generate_summary(BookEntity(id=book_id, **updated_book.model_dump()))
            else:
                updated_book.summary = existing_book.summary

            updated_entity = BookEntity(id=book_id, **updated_book.model_dump())
            BOOKS[index] = updated_entity
            return updated_entity

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            del BOOKS[index]
            return
    raise HTTPException(status_code=404, detail="Book not found")