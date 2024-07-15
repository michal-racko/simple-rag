import uuid
import datetime as dt

import pytest
import sqlalchemy

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


@pytest.fixture
def question_1(db_session, conversation) -> Question:
    question = Question(
        conversation_id=conversation.id,
        text='What\'s the day tomorrow?'
    )
    db_session.add(question)
    db_session.commit()
    return question


@pytest.fixture
def question_2(db_session, conversation) -> Question:
    question = Question(
        conversation_id=conversation.id,
        text='What\'s the day after tomorrow?'
    )
    db_session.add(question)
    db_session.commit()
    return question


@pytest.fixture
def answer(db_session, question) -> Answer:
    answer = Answer(
        question_id=question.id,
        text=f'Today is {dt.datetime.now().strftime("%A")}',
    )
    db_session.add(answer)
    db_session.commit()
    return answer


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


def test_conversation_unique_constraint(db_session, conversation):
    other_instance = Conversation(
        id=conversation.id
    )
    db_session.add(other_instance)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db_session.commit()


def test_read_conversation(db_session, conversation):
    other_instance = db_session.query(Conversation).filter_by(
        id=conversation.id
    ).first()
    assert other_instance == conversation


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


def test_question_unique_constraint(db_session, question, conversation):
    other_instance = Question(
        id=question.id,
        conversation_id=conversation.id,
        text='What\'s the day tomorrow?'
    )
    db_session.add(other_instance)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db_session.commit()


def test_question_foreign_key_constraint(db_session):
    question = Question(
        conversation_id=str(uuid.uuid4()),
        text='What\'s the day today?'
    )
    db_session.add(question)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db_session.commit()


def test_read_questions(db_session,
                        question,
                        question_1,
                        question_2,
                        conversation):
    questions = db_session.query(Question).filter_by(
        conversation_id=conversation.id
    ).all()
    assert set(questions) == {question, question_1, question_2}


def test_question_missing_conversation(db_session):
    question = Question(
        text='What\'s the day today?'
    )
    db_session.add(question)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db_session.commit()


def test_answer_schema(db_session, question):
    answer = Answer(
        question_id=question.id,
        text=f'Today is {dt.datetime.now().strftime("%A")}',
    )
    db_session.add(answer)
    db_session.commit()

    assert isinstance(answer.id, int)
    assert isinstance(answer.text, str)
    assert isinstance(answer.created_at, dt.datetime)
    assert answer.created_at < dt.datetime.now()


def test_answer_foreign_key_constraint(db_session):
    answer = Answer(
        question_id=-1,
        text=f'Today is {dt.datetime.now().strftime("%A")}',
    )
    db_session.add(answer)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db_session.commit()


def test_answer_missing_question(db_session):
    answer = Answer(
        text=f'Today is {dt.datetime.now().strftime("%A")}',
    )
    db_session.add(answer)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db_session.commit()


def test_read_answer(db_session, question, answer):
    other_instance = db_session.query(Answer).filter_by(
        question_id=question.id
    ).first()
    assert other_instance == answer


def test_single_answer_per_question(db_session, question, answer):
    other_answer = Answer(
        question_id=question.id,
        text=f'Again, today is {dt.datetime.now().strftime("%A")}',
    )
    db_session.add(other_answer)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db_session.commit()
