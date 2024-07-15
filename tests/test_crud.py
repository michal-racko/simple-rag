import uuid
import pytest

import api.v1.schemas as schemas
import db.models as models
from api.v1.crud import (
    create_conversation,
    get_conversation,
    update_conversation,
    answer_conversation
)
from api.v1.settings import TooManyQuestions


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
    conversation = create_conversation(
        db_session,
        api_question
    )
    _db_conversation = db_session.query(models.Conversation).filter(
        models.Conversation.id == conversation.id
    ).first()
    assert _db_conversation is not None

    db_questions = db_session.query(models.Question).filter(
        models.Question.conversation_id == conversation.id
    ).all()
    assert len(db_questions) == 1
    assert db_questions[0].answer_id is None

    assert conversation == schemas.Conversation(
        id=_db_conversation.id,
        questions=[api_question]
    )


def test_get_conversation(db_session,
                          db_conversation,
                          db_question,
                          db_question_1,
                          db_question_2,
                          db_answer,
                          db_answer_1):
    conversation = get_conversation(db_session, db_conversation.id)
    assert conversation.id == db_conversation.id
    assert len(conversation.questions) == 3

    assert conversation.questions[0].text == db_question.text
    assert conversation.questions[0].answer == db_answer.text
    assert conversation.questions[1].text == db_question_1.text
    assert conversation.questions[1].answer == db_answer_1.text
    assert conversation.questions[2].text == db_question_2.text
    assert conversation.questions[2].answer is None


def test_get_conversation_wrong_id(db_session):
    conversation = get_conversation(db_session, str(uuid.uuid4()))
    assert conversation is None


def test_update_conversation(db_session,
                             db_conversation,
                             db_question,
                             db_question_1,
                             db_answer,
                             db_answer_1,
                             api_question):
    conversation = update_conversation(
        db_session,
        db_conversation.id,
        api_question
    )
    assert conversation.questions[-1] == api_question

    questions = db_session.query(models.Question).filter(
        models.Question.conversation_id == conversation.id
    ).all()
    assert len(questions) == 3
    assert questions[-1].text == api_question.text


def test_update_conversation_wrong_id(db_session, api_question):
    conversation = update_conversation(
        db_session,
        str(uuid.uuid4()),
        api_question
    )
    assert conversation is None


def test_update_conversation_too_many_questions(db_session,
                                                db_conversation,
                                                api_question):
    for i in range(5):
        db_question = models.Question(
            conversation_id=db_conversation.id,
            text=f'Question {i}'
        )
        db_session.add(db_question)
        db_session.commit()

    with pytest.raises(TooManyQuestions):
        update_conversation(
            db_session,
            db_conversation.id,
            api_question
        )


def test_answer_conversation(db_session,
                             db_conversation,
                             db_question,
                             db_question_1,
                             db_question_2,
                             db_answer,
                             db_answer_1,
                             chatbot_response):
    conversation = answer_conversation(
        db_session,
        db_conversation.id,
        chatbot_response
    )
    assert conversation.id == db_conversation.id
    assert len(conversation.questions) == 3

    questions = db_session.query(models.Question).filter(
        models.Question.conversation_id == conversation.id
    ).all()
    assert len(questions) == 3
    answer = db_session.query(models.Answer).filter(
        models.Answer.id == questions[-1].answer_id
    ).first()

    assert answer is not None
    assert answer.text == chatbot_response
