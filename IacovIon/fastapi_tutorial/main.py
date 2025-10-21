from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()
CSV_FILE = "books.csv"

# Book validation
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["id", "title", "author", "year", "isbn"])
    df.to_csv(CSV_FILE, index=False)

# Book model
class Book(BaseModel):
    title: str
    author: str
    year: int
    isbn: str

def load_books():
    return pd.read_csv(CSV_FILE)

def save_books(df):
    df.to_csv(CSV_FILE, index=False)

@app.post("/books/")
def create_book(book: Book):
    df = load_books()
    new_id = int(df["id"].max()) + 1 if not df.empty else 1
    new_book = {
        "id": new_id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn
    }
    df = pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)
    save_books(df)
    return new_book

@app.get("/books/")
def get_all_books():
    df = load_books()
    return df.to_dict(orient="records")

@app.get("/books/{book_id}")
def get_book(book_id: int):
    df = load_books()
    book = df.loc[df["id"] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.iloc[0].to_dict()

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    df = load_books()
    if book_id not in df["id"].values:
        raise HTTPException(status_code=404, detail="Book not found")

    df.loc[df["id"] == book_id, ["title", "author", "year", "isbn"]] = [
        updated_book.title,
        updated_book.author,
        updated_book.year,
        updated_book.isbn
    ]
    save_books(df)
    return df[df["id"] == book_id].iloc[0].to_dict()

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    df = load_books()
    if book_id not in df["id"].values:
        raise HTTPException(status_code=404, detail="Book not found")
    df = df.loc[df["id"] != book_id]
    save_books(df)
    return {"message": f"Book with id {book_id} deleted successfully"}
