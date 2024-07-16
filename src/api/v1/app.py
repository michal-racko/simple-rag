import time
import chromadb
import requests
from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from db import SessionLocal, engine, Base
from .schemas import Conversation, Question
from .crud import (
    create_conversation,
    get_conversation,
    update_conversation,
    answer_conversation
)
from .settings import (
    TooManyQuestions,
    SIMPLE_RAG_RUN_ID,
    SIMPLE_RAG_SIMILARITY_THRESHOLD,
    SIMPLE_RAG_EMBEDDING_URL,
    SIMPLE_RAG_EMBEDDING_MODEL,
    SIMPLE_RAG_LLM_URL,
    SIMPLE_RAG_LLM_MODEL
)
from .templates import NO_SALE_PROMPT_TEMPLATE, GENERAL_PROMPT_TEMPLATE

for _ in range(10):
    try:
        Base.metadata.create_all(bind=engine)
        break
    except Exception:
        time.sleep(1)
else:
    raise RuntimeError('Cannot connect to database')

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


chroma_client = chromadb.PersistentClient(
    path=str(Path(__file__).parent.parent.parent / 'data' / 'chroma-db'),
)
chroma_collection = chroma_client.get_collection(
    f'company-documents-{SIMPLE_RAG_RUN_ID}'
)


def _request_rag(query: str, previous_questions: list[Question] = None) -> str:
    global chroma_collection

    try:
        response = requests.post(
            SIMPLE_RAG_EMBEDDING_URL,
            json={
                'model': SIMPLE_RAG_EMBEDDING_MODEL,
                'prompt': query
            }
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail='embedding model error')
    if response.status_code != 200:
        raise HTTPException(status_code=503, detail='embedding model error')

    results = chroma_collection.query(response.json()['embedding'], n_results=1)
    distance = results['distances'][0][0]

    if distance < SIMPLE_RAG_SIMILARITY_THRESHOLD:
        prompt = NO_SALE_PROMPT_TEMPLATE.format(question=query, document=
        results['documents'][0][0])
    else:
        prompt = GENERAL_PROMPT_TEMPLATE.format(question=query)

    previous_messages = []
    if previous_questions:
        for question in previous_questions:
            previous_messages.append({
                'role': 'user',
                'content': question.text
            })
            previous_messages.append({
                'role': 'assistant',
                'content': question.answer
            })

    try:
        response = requests.post(
            SIMPLE_RAG_LLM_URL,
            json={
                'model': SIMPLE_RAG_LLM_MODEL,
                'stream': False,
                'messages': previous_messages + [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            }
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail='embedding model error')
    if response.status_code != 200:
        raise HTTPException(status_code=503, detail='llm model error')

    return response.json()['message']['content']


@app.post('/conversations/', status_code=status.HTTP_201_CREATED)
async def view_post_conversation(question: Question,
                                 db: Session = Depends(get_db)) -> Conversation:
    conversation = create_conversation(db, question)
    rag_response = _request_rag(question.text)
    return answer_conversation(db, conversation.id, rag_response)


@app.get('/conversations/{conversation_id}')
async def view_get_conversation(conversation_id: str,
                                db: Session = Depends(get_db)) -> Conversation:
    conversation = get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail='Conversation not found')
    return conversation


@app.put('/conversations/{conversation_id}')
async def view_put_conversation(conversation_id: str,
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

    rag_response = _request_rag(question.text)
    return answer_conversation(db, conversation.id, rag_response)
