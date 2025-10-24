from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
import os

SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@db:5432/mydatabase"
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()


class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    completed = Column(Boolean, default=False)
    created_at = Column(String)

def __repr__(self):
    return f"Task(id={self.id!r}, name={self.name!r})"

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Databse tables intialized")

async def get_db():
    db=AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

