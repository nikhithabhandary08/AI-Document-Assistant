from fastapi import FastAPI, File, UploadFile
from pathlib import Path

from backend.services.document_service import extract_text_from_pdf
from backend.services.rag_service import retrieve_relevant_chunks
from backend.services.llm_service import generate_answer
from backend.models.request_models import QuestionRequest


app = FastAPI(title="AI Document Assistant")


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

    return {
        "filename": file.filename,
        "message": "Document uploaded and text extracted successfully!",
        "text_length": len(extracted_text),
    }


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    upload_dir = Path("data/uploads")
    pdf_files = list(upload_dir.glob("*.pdf"))

    if not pdf_files:
        return {"answer": "No PDF document has been uploaded yet."}

    latest_pdf = max(pdf_files, key=lambda path: path.stat().st_mtime)

    text = extract_text_from_pdf(str(latest_pdf))
    chunks = retrieve_relevant_chunks(text, request.question, top_k=3)
    answer = generate_answer(request.question, chunks)

    return {
        "question": request.question,
        "answer": answer,
    }