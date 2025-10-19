from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        DATABASE_URL = os.getenv("DATABASE_URL")
        self.engine = create_engine(DATABASE_URL)
        self.db_session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()
    
    def get_db(self):
        db = self.db_session()
        try:
            yield db
        finally:
            db.close()
    
    def create_tables(self):
        self.Base.metadata.create_all(bind=self.engine)