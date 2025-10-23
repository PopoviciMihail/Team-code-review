from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status, Response
from fastapi.responses import RedirectResponse
from pydantic import AfterValidator
from Model.book import Book
from Repository.book_csv_repository import CSV_Repository

book_router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

book_repository = CSV_Repository()


def check_valid_isbn(book: Book):
    isbn_lower = book.isbn.lower()
    if not any(prefix in isbn_lower for prefix in ['isbn', '978', '979', 'imdb']):
        raise ValueError('ISBN should contain "isbn", "978", "979", or "imdb"')
    return book.isbn


@book_router.get("/", response_model=list[Book])
async def get_all_books() -> list[Book]:
    """Retrieve all books from the CSV."""
    return book_repository.get_all()


@book_router.get("/{book_id}", response_model=Book)
async def get_book_by_id(book_id: Annotated[int, Path(title="ID of the needed book", gt=0)]) -> Book:
    """Get a single book by ID."""
    book = book_repository.get(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return book


@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book) -> Book:
    """Create a new book entry."""
    try:
        created_book = book_repository.add(book)
        return created_book
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating book: {str(e)}"
        )


@book_router.put("/{book_id}", response_model=Book)
async def update_book(
    book_id: Annotated[int, Path(title="ID of the needed book", gt=0)],
    book: Annotated[Book, AfterValidator(check_valid_isbn)]
) -> Book:
    """Update an existing book."""
    updated_book = book_repository.update(book_id, book)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} was not found when trying to update it"
        )
    return updated_book


@book_router.delete("/{book_id}")
async def delete_book(book_id: int):
    """Delete a book by ID."""
    success = book_repository.remove(book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} was not found when trying to delete it"
        )
    return {"message": f"Book with ID {book_id} deleted successfully"}


@book_router.get("/stats/")
async def get_books_statistics():
    """Get statistics about the books collection using pandas."""
    return book_repository.get_books_statistics()


@book_router.get("/surprise")
async def surprise() -> Response:
    """A simple surprise..."""
    return RedirectResponse("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
