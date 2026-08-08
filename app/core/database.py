from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import settings


class Database:
    def __init__(self, db_url: str, echo: bool = False):
        self._engine = create_async_engine(db_url, echo=echo, pool_pre_ping=True)
        self._session: AsyncSession = async_sessionmaker(
            bind=self._engine, autocommit=False
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession]:
        session = self._session()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def get_db(self) -> AsyncSession:
        async with self.session() as session:
            yield session


database = Database(settings.database_settings.db_url.unicode_string())
