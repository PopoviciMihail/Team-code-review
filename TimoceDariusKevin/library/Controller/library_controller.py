from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from Model.user import User
from Model.book import Book
from Model.user_book import UserBook
from Service.authentication import get_current_active_user, require_admin
from Database.SqlEngine import SessionDependency

library_router = APIRouter(
    prefix="/library",
    tags=["Personal Library"]
)

@library_router.post("/{book_id}")
async def add_to_library(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDependency,
    book_id: int
):
    """Add a book to user's personal library"""
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.quantity <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    
    # Check if book already in library
    existing = session.exec(
        select(UserBook).where(
            UserBook.user_id == current_user.id,
            UserBook.book_id == book_id
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Book already in library")
    
    # Reduce available quantity
    book.quantity -= 1
    
    user_book = UserBook(user_id=current_user.id, book_id=book_id)
    session.add(user_book)
    session.add(book)
    session.commit()
    
    return {"message": "Book added to library"}

@library_router.get("/my-books")
async def get_my_library(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDependency
):
    """Get current user's personal library"""
    user_books = session.exec(
        select(UserBook).where(UserBook.user_id == current_user.id)
    ).all()
    
    books = []
    for user_book in user_books:
        book = session.get(Book, user_book.book_id)
        if book:
            books.append(book)
    
    return books

@library_router.get("/user/{user_id}")
async def get_user_library(
    current_user: Annotated[User, Depends(require_admin)],
    session: SessionDependency,
    user_id: int
):
    """Get any user's personal library - Admin only"""
    user_books = session.exec(
        select(UserBook).where(UserBook.user_id == user_id)
    ).all()
    
    books = []
    for user_book in user_books:
        book = session.get(Book, user_book.book_id)
        if book:
            books.append(book)
    
    return books

@library_router.delete("/{book_id}")
async def remove_from_library(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDependency,
    book_id: int
):
    """Remove a book from user's personal library"""
    user_book = session.exec(
        select(UserBook).where(
            UserBook.user_id == current_user.id,
            UserBook.book_id == book_id
        )
    ).first()
    
    if not user_book:
        raise HTTPException(status_code=404, detail="Book not in library")
    
    # Return book to available quantity
    book = session.get(Book, book_id)
    if book:
        book.quantity += 1
        session.add(book)
    
    session.delete(user_book)
    session.commit()
    
    return {"message": "Book removed from library"}