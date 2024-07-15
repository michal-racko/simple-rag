from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal, engine, Base
from .schemas import Conversation, Question
from .crud import create_conversation, get_conversation, update_conversation
from .settings import TooManyQuestions

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/conversations/')
def view_post_conversation(question: Question,
                           db: Session = Depends(get_db)) -> Conversation:
    conversation = create_conversation(db, question)
    # call ollama here
    return conversation


@app.get('/conversations/{conversation_id}')
def view_get_conversation(conversation_id: str,
                          db: Session = Depends(get_db)) -> Conversation:
    conversation = get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail='Conversation not found')
    return conversation


@app.put('/conversations/{conversation_id}')
def view_put_conversation(conversation_id: str,
                          question: Question,
                          db: Session = Depends(get_db)) -> Conversation:
    try:
        conversation = update_conversation(db, conversation_id, question)
    except TooManyQuestions:
        raise HTTPException(
            status_code=429,
            detail='Question limit for this conversation exceeded'
        )

    if not conversation:
        raise HTTPException(status_code=404, detail='Conversation not found')
    return conversation
