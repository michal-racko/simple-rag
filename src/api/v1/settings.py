import os

SIMPLE_RAG_MAX_QUESTIONS = int(
    os.environ.get(
        'SIMPLE_RAG_MAX_QUESTIONS',
        5
    )
)


class TooManyQuestions(Exception):
    """
    To be raised when the user asks more questions than the above-defined limit
    """
    pass


SIMPLE_RAG_EMBEDDING_URL = os.environ.get(
    'SIMPLE_RAG_EMBEDDING_URL',
    'http://localhost:11434/api/embeddings'
)

SIMPLE_RAG_EMBEDDING_MODEL = os.environ.get(
    'SIMPLE_RAG_EMBEDDING_MODEL',
    'mxbai-embed-large'
)

SIMPLE_RAG_LLM_URL = os.environ.get(
    'SIMPLE_RAG_LLM_URL',
    'http://localhost:11434/api/chat'
)

SIMPLE_RAG_LLM_MODEL = os.environ.get(
    'SIMPLE_RAG_LLM_MODEL',
    'llama3:8b'
)

SIMPLE_RAG_RUN_ID = os.environ.get(
    'SIMPLE_RAG_RUN_ID',
    'd46674dd-c854-4335-b986-1de579166728'
)

SIMPLE_RAG_SIMILARITY_THRESHOLD = int(
    os.environ.get(
        'SIMPLE_RAG_SIMILARITY_THRESHOLD',
        335
    )
)
