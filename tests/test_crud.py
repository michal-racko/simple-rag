import pytest
import datetime as dt

import api.v1.schemas as schemas
import db.models as models
from api.v1.crud import create_conversation, get_conversation, create_answer


@pytest.fixture
def api_question() -> schemas.Question:
    return schemas.Question(
        text='Can I change my delivery address after placing an order?'
    )


@pytest.fixture
def chatbot_response() -> str:
    return (
        'Yes, you can change your delivery address after placing an order. '
        'Please contact our customer service team as soon as possible '
        'to update your details.'
    )


def test_create_conversation(db_session, api_question):
    conversation, question = create_conversation(
        db_session,
        api_question
    )
    assert conversation is not None
    assert conversation.created_at < dt.datetime.now()

    db_questions = db_session.query(models.Question).filter(
        conversation.id == conversation.id
    ).all()
    assert db_questions == [question]
    assert db_questions[0].answer_id is None


def test_get_conversation(db_session,
                          db_conversation,
                          db_question,
                          db_question_1,
                          db_question_2,
                          db_answer,
                          db_answer_1,
                          db_answer_2):
    conversation = get_conversation(db_session, db_conversation.id)
    assert conversation.id == db_conversation.id
    assert len(conversation.questions) == 3

    assert conversation.questions[0].text == db_question.text
    assert conversation.questions[0].answer == db_answer.text
    assert conversation.questions[1].text == db_question_1.text
    assert conversation.questions[1].answer == db_answer_1.text
    assert conversation.questions[2].text == db_question_2.text
    assert conversation.questions[2].answer == db_answer_2.text


def test_create_answer(db_session, db_question, chatbot_response):
    create_answer(db_session, db_question, chatbot_response)

    _db_question = db_session.query(models.Question).filter(
        models.Question.id == db_question.id
    ).first()
    assert _db_question.answer_id is not None

    _db_answer = db_session.query(models.Answer).filter(
        models.Answer.id == _db_question.answer_id
    ).first()
    assert _db_answer.text == chatbot_response
