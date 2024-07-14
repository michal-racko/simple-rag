import random

from pathlib import Path


def read_user_questions(
        file_path: Path,
        n: int = None,
        shuffle: bool = False,
        random_seed: int = None,
) -> list[str]:
    questions = file_path.read_text().strip().split('\n')
    if shuffle:
        random.seed(random_seed)
        random.shuffle(questions)
    if n is None:
        return questions
    else:
        return questions[:n]
