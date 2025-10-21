from fastapi import FastAPI
from config.database import Database
from routers import books

database = Database()
database.create_tables()

app = FastAPI()
app.include_router(books.router)

@app.get("/")
def default_route():
    return {"App": "Is running"}