from collections import namedtuple
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


class sqlalchemy_result:
    def __init__(self, rows):
        self.rows = [row[0] for row in rows]

    def rows2dict(self):
        return [
            {col.name: getattr(row, col.name) for col in row.__table__.columns}
            for row in self.rows
        ]

    def rows2tuple(self):
        columns = [col.name for col in self.rows[0].__table__.columns]
        Record = namedtuple("Record", columns)
        return [
            Record(*[getattr(row, col.name) for col in row.__table__.columns])
            for row in self.rows
        ]


"""Our Database Engines"""
DISCORD_ENGINE = Engine()
