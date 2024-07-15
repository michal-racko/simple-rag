from sqlalchemy.orm import Session

import api.v1.schemas as schemas
import db.models as models


def create_conversation(db: Session,
                        question: schemas.Question) -> (
        models.Conversation,
        models.Question
):
    conversation = models.Conversation()
    db.add(conversation)
    db.commit()

    db_question = models.Question(
        text=question.text,
        conversation_id=conversation.id
    )
    db.add(db_question)
    db.commit()

    return conversation, db_question


def get_conversation(db: Session, conversation_id: str) -> schemas.Conversation:
    db_conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()
    return schemas.Conversation(
        id=db_conversation.id,
        questions=[
            schemas.Question(
                text=db_question.text,
                answer=db_answer.text if db_answer is not None else None,
            )
            for db_question, db_answer in db.query(
                models.Question,
                models.Answer
            ).filter(
                models.Question.conversation_id == db_conversation.id
            ).filter(
                models.Question.answer_id == models.Answer.id
            ).all()
        ]
    )


def create_answer(db: Session,
                  db_question: models.Question,
                  text: str) -> (models.Answer, models.Question):
    db_answer = models.Answer(text=text)
    db.add(db_answer)
    db.commit()

    db_question.answer_id = db_answer.id
    db.commit()
    return db_answer, db_question
