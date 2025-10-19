from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Book
import pandas as pd
from database import Database
from schemas import BookRequest
import requests

app = FastAPI()
database = Database()
database.create_tables()

@app.post("/books/")
def create_book(book_data: BookRequest, db: Session = Depends(database.get_db)):
    existing_book = db.query(Book).filter(Book.isbn == book_data.isbn).first()

    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists!")
    
    book = Book(
        title = book_data.title,
        author = book_data.author,
        year = book_data.year,
        isbn = book_data.isbn
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn
    }

@app.get("/books/")
def read_books(db: Session = Depends(database.get_db)):
    books = db.query(Book).all()
    return books if books else {"No": "books to show"}
    
@app.get("/books/{book_id}")
def read_book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}")
def update_book(book_data: BookRequest, book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found!")
    
    book.title = book_data.title
    book.author = book_data.author
    book.year = book_data.year
    book.isbn = book_data.isbn

    db.commit()

    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn
    }

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Not found")
    
    db.delete(book)
    db.commit()
    return {"Book": "deleted succesfully!"}

@app.get("/")
def default_route():
    return {"App": "Is running"}