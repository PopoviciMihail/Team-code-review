from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status, Response
from fastapi.responses import RedirectResponse
from sqlmodel import select
from Model.book import Book, BookBase
from Repository.book_csv_repository import CSV_Repository
from Database.SqlEngine import SessionDependency
from Model.user import User
from Service.authentication import get_current_active_user
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import RedirectResponse
from Model.book import Book, BookPublic, PrivilegedBook, BookCreate
from Model.user import User, RoleType
from Service.authentication import get_current_active_user, require_privileged
from Database.SqlEngine import SessionDependency
from sqlmodel import select
book_router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

book_repository = CSV_Repository()

def check_valid_isbn(book: BookBase):
    isbn_lower = book.isbn.lower()
    if not any(prefix in isbn_lower for prefix in ['isbn', '978', '979', 'imdb']):
        raise ValueError('ISBN should contain "isbn", "978", "979", or "imdb"')
    return book.isbn


@book_router.get("/", response_model=list[Book])
async def get_all_books(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDependency,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    sort_by: str | None = Query(None, description="Field to sort by"),
    author_filter: str | None = Query(None, description="Filter by author")
    ) -> list[Book]:
    """Retrieve all books with pagination and filtering."""
    query = select(Book)
    
    if author_filter:
        query = query.where(Book.author == author_filter)
    if sort_by and hasattr(Book, sort_by):
        query = query.order_by(getattr(Book, sort_by))
    else:
        query = query.order_by(Book.title)
    
    books = session.exec(query.offset(offset).limit(limit)).all()
    
    result = []
    for book in books:
        if current_user.role == RoleType.Privileged:
            result.append(PrivilegedBook(
                id=book.id,
                title=book.title,
                author=book.pseudonym or book.author,  # Show pseudonym to privileged
                author_true=book.author,  # Show true author only to privileged
                pseudonym=book.pseudonym,
                year=book.year,
                isbn=book.isbn,
                quantity=book.quantity
            ))
        else:
            result.append(BookPublic(
                id=book.id,
                title=book.title,
                author=book.pseudonym or book.author,  # Show pseudonym to others
                pseudonym=book.pseudonym,
                year=book.year,
                isbn=book.isbn,
                quantity=book.quantity
            ))
    return result


@book_router.get("/{book_id}", response_model=BookPublic)
async def get_book_by_id(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDependency,
    book_id: Annotated[int, Path(title="ID of the needed book", gt=0)]):
    """Get a single book by ID."""
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    if current_user.role == RoleType.Privileged:
        return PrivilegedBook(
           id=book.id,
            title=book.title,
            author=book.pseudonym or book.author,
            author_true=book.author,
            pseudonym=book.pseudonym,
            year=book.year,
            isbn=book.isbn,
            quantity=book.quantity 
        )
    else:
        return BookPublic(
            id=book.id,
            title=book.title,
            author=book.pseudonym or book.author,
            pseudonym=book.pseudonym,
            year=book.year,
            isbn=book.isbn,
            quantity=book.quantity
        )

@book_router.post("/", response_model=BookPublic, status_code=status.HTTP_201_CREATED)
async def create_book(
    current_user: Annotated[User, Depends(require_privileged)],
    session: SessionDependency,
    book: BookCreate
):
    if book.quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")
    
    try:
        check_valid_isbn(book)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    db_book = Book(**book.model_dump())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    
    return BookPublic(**db_book.model_dump())



@book_router.put("/{book_id}", response_model=BookPublic)
async def update_book(
    current_user: Annotated[User, Depends(require_privileged)],
    session: SessionDependency,
    book_id: Annotated[int, Path(title="ID of the needed book", gt=0)],
    book: BookCreate
):
    """Update an existing book - only for privileged users and admins."""
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} was not found"
        )
    
    try:
        check_valid_isbn(book)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    
    return BookPublic(**db_book.model_dump())

@book_router.delete("/{book_id}")
async def delete_book(
    current_user: Annotated[User, Depends(require_privileged)],
    session: SessionDependency,
    book_id: int
):
    """Delete a book by ID - only for privileged users and admins."""
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} was not found"
        )
    
    session.delete(book)
    session.commit()
    return {"message": f"Book with ID {book_id} deleted successfully"}

@book_router.get("/stats/")
async def get_books_statistics():
    """Get statistics about the books collection using pandas."""
    return book_repository.get_books_statistics()


@book_router.get("/surprise")
async def surprise() -> Response:
    """A simple surprise..."""
    return RedirectResponse("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
