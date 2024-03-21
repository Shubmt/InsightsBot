from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from fastapi_utils.session import FastAPISessionMaker
from functools import lru_cache

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', pool_size=100, max_overflow=120)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.ModelBase = declarative_base()
        self._cached_fastapi_sessionmaker = None

    def get_db(self):
        yield from self._get_fastapi_sessionmaker().get_db()

    @lru_cache(maxsize=32)
    def _get_fastapi_sessionmaker(self) -> FastAPISessionMaker:
        if self._cached_fastapi_sessionmaker is None:
            self._cached_fastapi_sessionmaker = FastAPISessionMaker(self.engine.url)
            self._cached_fastapi_sessionmaker._cached_engine = self.engine
        return self._cached_fastapi_sessionmaker
