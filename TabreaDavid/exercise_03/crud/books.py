from sqlalchemy.orm import Session
from db.models import Book
from routers.schemas import BookRequest


def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def get_book_by_isbn(db: Session, isbn: str):
    return db.query(Book).filter(Book.isbn == isbn).first()

def get_all_books(db: Session):
    return db.query(Book).all()


def create_book(db: Session, book_data: BookRequest):
    book = Book(
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
        isbn=book_data.isbn
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book_id: int, book_data: BookRequest):
    book = get_book_by_id(db, book_id)
    if book:
        book.title = book_data.title
        book.author = book_data.author
        book.year = book_data.year
        book.isbn = book_data.isbn
        db.commit()
        db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    book = get_book_by_id(db, book_id)
    if book:
        db.delete(book)
        db.commit()
        return True
    return False
