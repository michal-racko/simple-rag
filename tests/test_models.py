import uuid
import datetime as dt

import pytest

from db.models import Conversation, Question, Answer


@pytest.fixture
def conversation(db_session) -> Conversation:
    conversation = Conversation()
    db_session.add(conversation)
    db_session.commit()
    return conversation


@pytest.fixture
def question(db_session, conversation) -> Question:
    question = Question(
        conversation_id=conversation.id,
        text='What\'s the day today?'
    )
    db_session.add(question)
    db_session.commit()
    return question


def is_valid_uuid4(value: str) -> bool:
    try:
        uuid_obj = uuid.UUID(value, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == value


def test_conversation_schema(db_session):
    conversation = Conversation()
    db_session.add(conversation)
    db_session.commit()

    assert isinstance(conversation.id, str)
    assert is_valid_uuid4(conversation.id)

    assert isinstance(conversation.started_at, dt.datetime)
    assert conversation.started_at < dt.datetime.now()


def test_question_schema(db_session, conversation):
    question = Question(
        conversation_id=conversation.id,
        text='What\'s the day today?'
    )
    db_session.add(question)
    db_session.commit()

    assert isinstance(question.id, int)
    assert isinstance(question.text, str)
    assert isinstance(question.created_at, dt.datetime)
    assert question.created_at < dt.datetime.now()


def test_answers_schema(db_session, question):
    answers = Answer(
        question_id=question.id,
        text=f'Today is {dt.datetime.now().strftime("%A")}',
    )
    db_session.add(answers)
    db_session.commit()

    assert isinstance(answers.id, int)
    assert isinstance(answers.text, str)
    assert isinstance(answers.created_at, dt.datetime)
    assert answers.created_at < dt.datetime.now()
