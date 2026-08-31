from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from backend.services.document_service import extract_text_from_pdf
from backend.services.rag_service import retrieve_from_saved_index
from backend.services.llm_service import generate_answer
from backend.models.request_models import QuestionRequest
from backend.services.indexing_service import index_document


app = FastAPI(title="AI Document Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "AI Document Assistant API is running!"}


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename

    with file_path.open("wb") as buffer:
        buffer.write(await file.read())

    extracted_text = extract_text_from_pdf(str(file_path))

    chunks_indexed = index_document(extracted_text)

    return {
    "filename": file.filename,
    "message": "Document uploaded and indexed successfully!",
    "text_length": len(extracted_text),
    "chunks_indexed": chunks_indexed,
}


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    index_path = Path("data/vectorstore/document.index")
    chunks_path = Path("data/vectorstore/chunks.json")

    if not index_path.exists() or not chunks_path.exists():
        return {"answer": "No indexed document is available yet."}

    chunks = retrieve_from_saved_index(request.question, top_k=3)
    answer = generate_answer(request.question, chunks)

    return {
        "question": request.question,
        "answer": answer,
    }