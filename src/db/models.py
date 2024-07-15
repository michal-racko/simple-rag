import uuid
import datetime as dt
from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    DateTime,
    ForeignKey
)

from db.settings import Base


class Conversation(Base):
    """
    Represents a conversation with the QnA chatbot.
    """

    __tablename__ = 'conversations'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    started_at = Column(DateTime, default=dt.datetime.utcnow)


class Question(Base):
    """
    Represents a question asked by the user.
    """

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    conversation_id = Column(
        String(36),
        ForeignKey('conversations.id'),
        nullable=False
    )


class Answer(Base):
    """
    Represents chatbot's answer to a given question.
    """

    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    question_id = Column(
        Integer,
        ForeignKey('questions.id'),
        nullable=False
    )
