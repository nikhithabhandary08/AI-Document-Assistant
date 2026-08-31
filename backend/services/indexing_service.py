from backend.services.chunking_service import chunk_text
from backend.services.embedding_service import generate_embeddings
from backend.services.vector_store import create_faiss_index, save_faiss_index
from backend.services.storage_service import save_chunks


INDEX_PATH = "data/vectorstore/document.index"
CHUNKS_PATH = "data/vectorstore/chunks.json"


def index_document(text: str) -> int:
    """Create and persist the vector index for a document."""

    chunks = chunk_text(text)

    if not chunks:
        return 0

    embeddings = generate_embeddings(chunks)
    index = create_faiss_index(embeddings)

    save_faiss_index(index, INDEX_PATH)
    save_chunks(chunks, CHUNKS_PATH)

    return len(chunks)