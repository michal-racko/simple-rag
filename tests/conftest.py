import os
import uuid
import datetime as dt

import pytest

from sqlalchemy.orm import sessionmaker

TEST_DB_PATH = f'/tmp/{uuid.uuid4()}-test.db'
os.environ['SIMPLE_RAG_TEST'] = 'True'
os.environ['SIMPLE_RAG_SQLITE_DB_PATH'] = TEST_DB_PATH

from db.settings import engine, Base
import api.v1.schemas as schemas
import db.models as models

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


@pytest.fixture
def db_conversation(db_session) -> models.Conversation:
    db_conversation = models.Conversation()
    db_session.add(db_conversation)
    db_session.commit()
    return db_conversation


@pytest.fixture
def db_answer(db_session) -> models.Answer:
    db_answer = models.Answer(
        text=f'Today is {dt.datetime.now().strftime("%A")}',
    )
    db_session.add(db_answer)
    db_session.commit()
    return db_answer


@pytest.fixture
def db_answer_1(db_session) -> models.Answer:
    db_answer = models.Answer(
        text='Tomorrow is '
             f'{(dt.datetime.now() + dt.timedelta(days=1)).strftime("%A")}',
    )
    db_session.add(db_answer)
    db_session.commit()
    return db_answer


@pytest.fixture(scope='function')
def db_question(db_session, db_conversation, db_answer) -> models.Question:
    db_question = models.Question(
        conversation_id=db_conversation.id,
        text='What\'s the day today?',
        answer_id=db_answer.id
    )
    db_session.add(db_question)
    db_session.commit()
    return db_question


@pytest.fixture
def db_question_1(db_session, db_conversation, db_answer_1) -> models.Question:
    db_question = models.Question(
        conversation_id=db_conversation.id,
        text='What\'s the day tomorrow?',
        answer_id=db_answer_1.id
    )
    db_session.add(db_question)
    db_session.commit()
    return db_question


@pytest.fixture
def db_question_2(db_session, db_conversation) -> models.Question:
    db_question = models.Question(
        conversation_id=db_conversation.id,
        text='What\'s the day after tomorrow?',
    )
    db_session.add(db_question)
    db_session.commit()
    return db_question
