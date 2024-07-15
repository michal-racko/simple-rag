from sqlalchemy.orm import Session

import api.v1.schemas as schemas
import db.models as models
from api.v1.settings import SIMPLE_RAG_MAX_QUESTIONS, TooManyQuestions


def create_conversation(db: Session,
                        question: schemas.Question) -> schemas.Conversation:
    db_conversation = models.Conversation()
    db.add(db_conversation)
    db.commit()

    db_question = models.Question(
        text=question.text,
        conversation_id=db_conversation.id
    )
    db.add(db_question)
    db.commit()

    return schemas.Conversation(
        id=db_conversation.id,
        questions=[
            schemas.Question(text=db_question.text)
        ]
    )


def _get_api_conversation(db: Session,
                          conversation_id: str) -> schemas.Conversation:
    """
    Retrieves questions and answers for the given conversation and puts them
    into a schemas.Conversation object.
    """
    return schemas.Conversation(
        id=conversation_id,
        questions=[
            schemas.Question(
                text=db_question.text,
                answer=db_answer.text if db_answer is not None else None,
            )
            for db_question, db_answer in db.query(
                models.Question,
                models.Answer
            ).outerjoin(
                models.Answer,
                models.Question.answer_id == models.Answer.id
            ).filter(
                models.Question.conversation_id == conversation_id
            ).all()
        ]
    )


def get_conversation(db: Session, conversation_id: str) -> schemas.Conversation:
    db_conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()
    if not db_conversation:
        return None
    return _get_api_conversation(db, db_conversation.id)


def update_conversation(db: Session,
                        conversation_id: str,
                        question: schemas.Question) -> schemas.Conversation:
    db_conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()
    if not db_conversation:
        return None

    questions = db.query(models.Question).filter(
        models.Question.conversation_id == conversation_id
    ).all()
    if len(questions) >= SIMPLE_RAG_MAX_QUESTIONS:
        raise TooManyQuestions

    db_question = models.Question(
        text=question.text,
        conversation_id=db_conversation.id
    )
    db.add(db_question)
    db.commit()

    return _get_api_conversation(db, db_conversation.id)


def create_answer(db: Session,
                  db_question: models.Question,
                  text: str) -> (models.Answer, models.Question):
    db_answer = models.Answer(text=text)
    db.add(db_answer)
    db.commit()

    db_question.answer_id = db_answer.id  # TODO
    db.commit()
    return db_answer, db_question
