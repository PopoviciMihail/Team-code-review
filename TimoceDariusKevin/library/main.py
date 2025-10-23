from fastapi import FastAPI
from Controller.book_controller import book_router
app = FastAPI(
    title="API to manage books in a library",
    version="1.0.1",
    docs_url="/"
)

app.include_router(book_router)