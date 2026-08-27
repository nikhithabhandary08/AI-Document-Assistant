import faiss
import numpy as np


def create_faiss_index(embeddings: list[list[float]]) -> faiss.IndexFlatL2:
    """Create a FAISS index from embedding vectors."""

    if not embeddings:
        raise ValueError("Embeddings cannot be empty.")

    vectors = np.array(embeddings, dtype="float32")

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    return index


def search_faiss_index(
    index: faiss.IndexFlatL2,
    query_embedding: list[float],
    chunks: list[str],
    top_k: int = 3,
) -> list[str]:
    """Find the most similar document chunks."""

    if not chunks:
        return []

    query_vector = np.array([query_embedding], dtype="float32")

    distances, indices = index.search(query_vector, min(top_k, len(chunks)))

    return [chunks[i] for i in indices[0] if i != -1]