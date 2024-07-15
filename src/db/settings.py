import os

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import declarative_base

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
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    raise NotImplementedError

Base = declarative_base()
