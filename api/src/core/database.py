from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from .config import SessionLocal

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session