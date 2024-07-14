from pathlib import Path


def read_user_questions(file_path: Path, n: int = None) -> list[str]:
    questions = file_path.read_text().strip().split('\n')
    if n is None:
        return questions
    else:
        return questions[:n]
