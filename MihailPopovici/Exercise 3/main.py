from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import requests

app = FastAPI(
    title="Library Book Management API",
    version="1.0",
    docs_url="/"
)

class Book(BaseModel):
    title:str
    author:str
    year:int
    isbn:str

# DB Simulation
books_db = {}
next_id = 1

def export_books_to_csv():
    if books_db:
        df = pd.DataFrame([{"id": k, **v} for k, v in books_db.items()])
        df.to_csv("books.csv", index=False)
    else:
        pd.DataFrame(columns=["id", "title", "author", "year", "isbn"]).to_csv("books.csv", index=False)

@app.get("/")
def root():
    return {"message": "Library API running!"}

@app.post("/books/", response_model=dict)
def create_book(book: Book):
    global next_id
    book_id = next_id
    next_id += 1
    books_db[book_id] = book.model_dump()
    export_books_to_csv()
    return {"id": book_id, **book.model_dump()}

@app.get("/books/", response_model=List[dict])
def read_all_books():
    if not books_db:
        return []
    export_books_to_csv()
    return [{"id": k, **v} for k, v in books_db.items()]

@app.get("/books/{book_id}", response_model=dict)
def read_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": book_id, **books_db[book_id]}

@app.put("/books/{book_id}", response_model=dict)
def update_book(book_id:int, book: Book):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db[book_id] = book.model_dump()
    export_books_to_csv()
    return {"id": book_id, **book.model_dump()}

@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id:int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    deleted_book = books_db.pop(book_id)
    export_books_to_csv()
    return {"message": f"Book with id {book_id} deleted successfully", "book": deleted_book}

@app.get("/stats")
def get_books_statistics():
    """
    Uses pandas to compute simple statistics about the stored books.
    """
    if not books_db:
        raise HTTPException(status_code=404, detail="No books in library")

    df = pd.DataFrame([v for v in books_db.values()])
    avg_year = df["year"].mean()
    oldest = df["year"].min()
    newest = df["year"].max()

    return {
        "total_books": len(df),
        "average_year": round(avg_year, 2),
        "oldest_year": int(oldest),
        "newest_year": int(newest)
    }

@app.get("/external/", response_model=dict)
def external_info(title:str):
    """Fetch external information about a book by its title."""

    url = "https://openlibrary.org/search.json"
    params = {"title": title, "limit": 1}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"External service error: {str(e)}")
    
    data=response.json()

    if not data.get("docs"):
        raise HTTPException(status_code=404, detail="Book not found in Open Library")

    book_info = data["docs"][0]
    return {
        "searched_title": title,
        "found_title": book_info.get("title"),
        "author": book_info.get("author_name", ["Unknown"])[0],
        "first_publish_year": book_info.get("first_publish_year", "N/A"),
    }