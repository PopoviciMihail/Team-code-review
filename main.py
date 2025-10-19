from fastapi import FastAPI
import pandas as pd
import requests

app = FastAPI()
books = {}

@app.post("/books/")
def create_book():
    pass

@app.get("/books/")
def read_books():
    pass

@app.get("/books/{book_id}")
def read_book():
    pass

@app.put("/books/{book_id}")
def update_book():
    pass

@app.delete("/books/{book_id}")
def delete_book():
    pass

@app.get("/")
def default_route():
    return {"App": "Is running"}