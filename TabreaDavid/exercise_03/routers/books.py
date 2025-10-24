from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from routers.dependencies import database
from routers.schemas import BookRequest, BookResponse
from crud import books as crud_books
import pandas as pd
import requests

router = APIRouter(
    prefix="/books",
    tags=["books"]
)


@router.post("/", response_model=BookResponse)
def create_book(book_data: BookRequest, db: Session = Depends(database.get_db)):
    existing_book = crud_books.get_book_by_isbn(db, book_data.isbn)
    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists!")
    
    book = crud_books.create_book(db, book_data)
    
    return book


@router.get("/")
def read_books(db: Session = Depends(database.get_db)):
    books = crud_books.get_all_books(db)
    return books if books else {"No": "books to show"}


@router.get("/stats")
def get_stats(db: Session = Depends(database.get_db)):
    """Simple analytics using pandas"""
    books = crud_books.get_all_books(db)
    if not books:
        return {"message": "No books"}
    
    df = pd.DataFrame([{"author": b.author, "year": b.year} for b in books])
    
    return {
        "total": len(df),
        "authors": df['author'].nunique(),
        "avg_year": df['year'].mean()
    }


@router.get("/{book_id}")
def read_book(book_id: int, db: Session = Depends(database.get_db)):
    book = crud_books.get_book_by_id(db, book_id)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_data: BookRequest, book_id: int, db: Session = Depends(database.get_db)):
    book = crud_books.update_book(db, book_id, book_data)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found!")
    
    return book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    success = crud_books.delete_book(db, book_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {"message": "Book deleted successfully!"}


@router.get("/fetch/{isbn}")
def fetch_book(isbn: str):
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    response = requests.get(url, timeout=5)
    
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Not found")
    
    data = response.json()
    return {"title": data.get("title"), "year": data.get("publish_date")}

