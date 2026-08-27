from fastapi import FastAPI, File, UploadFile
from pathlib import Path
from backend.services.document_service import extract_text_from_pdf

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
    "text_length": len(extracted_text)
    }