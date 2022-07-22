from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from src import config


class Engine:
    def __init__(self):
        self.connection_string = config.SQL_URI
        self.engine = self.__get_engine(self.connection_string)
        self.session = self.__get_session_factory(self.engine)

    def __get_engine(self, connection_string) -> AsyncEngine:
        engine = create_async_engine(
            connection_string,
            poolclass=QueuePool,
            pool_pre_ping=True,
            pool_size=100,
            max_overflow=5000,
            pool_recycle=3600,
        )
        return engine

    def __get_session_factory(self, engine) -> sessionmaker:
        # self.engine.echo = True
        session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        return session

    @asynccontextmanager
    async def get_session(self):
        yield self.session()


"""Our Database Engines"""
DISCORD_ENGINE = Engine()
