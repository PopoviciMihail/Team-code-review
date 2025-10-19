from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
db_session = sessionmaker(bind=engine)
base = declarative_base()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    base.metadata.create_all(bind=engine)