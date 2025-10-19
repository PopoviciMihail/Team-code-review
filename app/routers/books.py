from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from schemas import BookRequest, BookResponse
from crud import books as crud_books

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

database = Database()

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
