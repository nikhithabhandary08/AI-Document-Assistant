from fastapi import FastAPI, File, UploadFile
from pathlib import Path

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

    return {
        "filename": file.filename,
        "message": "Document uploaded successfully!"
    }