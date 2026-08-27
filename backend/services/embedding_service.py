from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of text chunks."""

    if not chunks:
        return []

    embeddings = model.encode(chunks)

    return embeddings.tolist()