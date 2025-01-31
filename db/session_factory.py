from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.config import engine

# from sqlalchemy.orm import sessionmaker


AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
