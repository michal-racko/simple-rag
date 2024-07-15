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
