# Create async engine
from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import config
from src.books.models import Book


# Engine Configuration
async_engine = AsyncEngine(
    create_engine(
    url=config.DATABASE_URL,
    echo=True
))

# Database Initialization
async def init_db():
    async with async_engine.begin() as conn:
        # Create all tables using SQLModel metadata
        await conn.run_sync(SQLModel.metadata.create_all)



# Session Dependency 
from typing import AsyncGenerator

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind = async_engine,
        class_ = AsyncSession,
        expire_on_commit = False,
        autoflush = False

    )

    async with Session() as session:
        yield session


