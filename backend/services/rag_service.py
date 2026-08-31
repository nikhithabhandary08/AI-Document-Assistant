from backend.services.chunking_service import chunk_text
from backend.services.embedding_service import generate_embeddings
from backend.services.vector_store import (
    create_faiss_index,
    search_faiss_index,
    load_faiss_index,
)
from backend.services.storage_service import load_chunks

def retrieve_relevant_chunks(text: str, query: str, top_k: int = 3) -> list[str]:
    """Retrieve the most relevant chunks for a user query."""

    chunks = chunk_text(text)

    if not chunks:
        return []

    embeddings = generate_embeddings(chunks)
    index = create_faiss_index(embeddings)

    query_embedding = generate_embeddings([query])[0]

    return search_faiss_index(
        index,
        query_embedding,
        chunks,
        top_k=top_k,
    )


INDEX_PATH = "data/vectorstore/document.index"
CHUNKS_PATH = "data/vectorstore/chunks.json"


def retrieve_from_saved_index(query: str, top_k: int = 3) -> list[str]:
    """Retrieve relevant chunks from the saved document index."""

    index = load_faiss_index(INDEX_PATH)
    chunks = load_chunks(CHUNKS_PATH)

    if not chunks:
        return []

    query_embedding = generate_embeddings([query])[0]

    return search_faiss_index(
        index,
        query_embedding,
        chunks,
        top_k=top_k,
    )