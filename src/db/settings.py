import os

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import declarative_base, sessionmaker

SIMPLE_RAG_TEST = (
        os.environ.get('SIMPLE_RAG_TEST', 'false').lower()
        in ('true', 't', '1', 'yes', 'y')
)

postgresql_db = os.environ.get('SIMPLE_RAG_POSTGRESQL_DB')
postgresql_user = os.environ.get('SIMPLE_RAG_POSTGRESQL_USER')
postgresql_pswd = os.environ.get('SIMPLE_RAG_POSTGRESQL_PSWD')
postgresql_host = os.environ.get('SIMPLE_RAG_POSTGRESQL_HOST')
postgresql_port = os.environ.get('SIMPLE_RAG_POSTGRESQL_PORT')

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
elif all(p is not None for p in
         (postgresql_db,
          postgresql_user,
          postgresql_pswd,
          postgresql_host,
          postgresql_port)):
    SQLALCHEMY_DATABASE_URL = (
        'postgresql+psycopg2://'
        f'{postgresql_user}:'
        f'{postgresql_pswd}@'
        f'{postgresql_host}:'
        f'{postgresql_port}/'
        f'{postgresql_db}'
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    raise NotImplementedError

if engine.driver == 'pysqlite':
    # Add foreign-key constraints for sqlite
    @event.listens_for(Engine, 'connect')
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()
