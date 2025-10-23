from fastapi import FastAPI
from Controller.book_controller import book_router
from Controller.authentication_controller import auth_router
from Controller.library_controller import library_router
from Controller.user_controller import user_router
from Database.SqlEngine import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="API to manage books in a library",
    version="1.0.1",
    docs_url="/"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(library_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()