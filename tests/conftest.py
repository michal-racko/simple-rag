import os
import uuid
import pytest

from sqlalchemy.orm import sessionmaker

TEST_DB_PATH = f'/tmp/{uuid.uuid4()}-test.db'
os.environ['SIMPLE_RAG_TEST'] = 'True'
os.environ['SIMPLE_RAG_SQLITE_DB_PATH'] = TEST_DB_PATH

from db.settings import engine, Base

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture
def db_session():
    try:
        db = TestingSessionLocal()
        Base.metadata.create_all(engine)
        yield db
    finally:
        db.close()


def pytest_sessionfinish(session, exitstatus):
    """
    Remove the test database when all tests are finished.
    """
    os.remove(TEST_DB_PATH)
