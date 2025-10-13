from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from conf import Config

DATABASE_URL: str = f"postgresql+asyncpg://{Config.DATABASE_USER}:{Config.DATABASE_PASSWORD}@{Config.DATABASE_URL}"
async_engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()


@asynccontextmanager
async def get_async_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
