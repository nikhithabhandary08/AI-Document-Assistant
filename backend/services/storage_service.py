import json
from pathlib import Path


def save_chunks(chunks: list[str], file_path: str) -> None:
    """Save document chunks to a JSON file."""

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)


def load_chunks(file_path: str) -> list[str]:
    """Load document chunks from a JSON file."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Chunks file not found: {file_path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)