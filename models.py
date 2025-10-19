from database import base
from sqlalchemy import Column, Integer, String

class Book(base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    isbn = Column(String)