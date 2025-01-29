from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
import os

DATABASE_URL = f"sqlite+aiosqlite:///database/test.db"  # SQLite URL for async connections

# Create async engine
engine = create_async_engine(DATABASE_URL)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Description: get_db will make the session open and close once the API call is completed
    """
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()