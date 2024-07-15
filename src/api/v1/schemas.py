from pydantic import BaseModel


class Question(BaseModel):
    text: str
    answer: str = None


class Conversation(BaseModel):
    id: str = None
    questions: list[Question] = None
