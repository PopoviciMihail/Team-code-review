from fastapi import FastAPI, HTTPException, status
from schemas import BookCreate, BookUpdate, Book

app :FastAPI = FastAPI(
    title="Books library API", 
    version="1.0",
    docs_url="/")

_BOOKS: dict[int, dict] = {}

def _get_or_404(book_id: int) -> dict:
    book = _BOOKS.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate):
    next_id = (max(_BOOKS.keys()) + 1) if _BOOKS else 1
    book = {
        "id": next_id,
        "title": payload.title,
        "author": payload.author,
        "year": payload.year,
        "isbn": payload.isbn,
    }
    _BOOKS[next_id] = book
    return book

@app.get("/books", response_model=list[Book])
def list_books():
    return list(_BOOKS.values())

@app.get("/books/{book_id}", response_model=Book)
def get_task(book_id: int):
    return _get_or_404(book_id)

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookUpdate):
    book = _get_or_404(book_id)
    updates = payload.model_dump(exclude_unset=True)
    if updates:
        book.update(updates)
    return book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    _get_or_404(book_id)
    del _BOOKS[book_id]
    return None
