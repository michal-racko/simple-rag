import os

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import declarative_base, sessionmaker

SIMPLE_RAG_TEST = (
        os.environ.get('SIMPLE_RAG_TEST', 'false').lower()
        in ('true', 't', '1', 'yes', 'y')
)

if SIMPLE_RAG_TEST:
    SQLITE_DB_PATH = os.environ.get(
        'SIMPLE_RAG_SQLITE_DB_PATH',
        f'{os.getcwd()}/dev.db'
    )
    SQLALCHEMY_DATABASE_URL = f'sqlite:///{SQLITE_DB_PATH}'

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )
    if engine.driver == 'pysqlite':
        # Add foreign-key constraints for sqlite
        @event.listens_for(Engine, 'connect')
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.close()
else:
    raise NotImplementedError

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()
