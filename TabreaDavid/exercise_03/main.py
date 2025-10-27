from fastapi import FastAPI
from routers.dependencies import database
from routers import books

database.create_tables()

app = FastAPI()
app.include_router(books.router)

@app.get("/")
def default_route():
    return {"App": "Is running"}