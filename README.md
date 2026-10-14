# AI Document Assistant

### Local LLM-Powered PDF Question Answering with Retrieval-Augmented Generation (RAG)

AI Document Assistant is a document question-answering application that allows users to upload PDF files and ask questions about their content. It combines PDF text extraction, text chunking, semantic embeddings, vector search, and a locally running Large Language Model (LLM) to retrieve relevant document information and generate answers.

The project is designed to demonstrate a complete Retrieval-Augmented Generation (RAG) workflow using Python, FastAPI, PyMuPDF, Sentence Transformers, FAISS, and Ollama. The browser-based interface is built with HTML, CSS, and JavaScript.

> **Project status:** Local development project. The exact behavior and setup instructions should be verified against the current code and dependency files before presenting this README as a verified deployment guide.

## Application Preview

Add screenshots of your working application in the `docs/screenshots/` directory and update the paths below when they are available.

### Document Upload

<!-- Add a screenshot at docs/screenshots/document-upload.png -->
![Document Upload](docs/screenshots/document-upload.png)

Upload a PDF through the web interface so the backend can extract and prepare its content for retrieval.

### Question and Answer Interface

<!-- Add a screenshot at docs/screenshots/question-answer.png -->
![Question and Answer](docs/screenshots/question-answer.png)

Ask a question about the uploaded document and view the question alongside the generated response.

## Project Overview

Reading long documents manually can be time-consuming, especially when a user needs a specific fact or explanation. AI Document Assistant provides a conversational interface for exploring PDF content.

The application follows a **Retrieval-Augmented Generation (RAG)** approach. Instead of sending an entire document to a language model for every question, the system prepares document text for search, retrieves chunks that are relevant to the user's question, and supplies those chunks as context to a local LLM.

The intended processing pipeline is:

1. A user uploads a PDF through the frontend.
2. The FastAPI backend receives the file.
3. PyMuPDF extracts text from the PDF.
4. The extracted text is split into smaller chunks.
5. Sentence Transformers converts chunks into embedding vectors.
6. FAISS indexes the vectors for similarity search.
7. A user submits a question.
8. The question is embedded and compared with the indexed document chunks.
9. Relevant chunks are selected and provided to the locally running Ollama model.
10. The model generates a response using the retrieved context, which is returned to the frontend.

This project demonstrates how document processing, vector retrieval, and LLM inference can be combined in one application. It does not guarantee that every generated answer is correct; answers should be checked against the source document when accuracy is important.

## Key Features

### PDF Upload and Text Extraction

- Accept PDF documents through the web interface.
- Send uploaded files to the FastAPI backend.
- Extract text from PDF pages using PyMuPDF.
- Prepare extracted content for downstream chunking and retrieval.
- Handle extraction errors through backend responses where implemented.

**Important:** PDFs that contain scanned page images rather than a text layer may require OCR. OCR support should not be assumed unless it is explicitly implemented.

### Text Chunking

- Split extracted document text into smaller sections.
- Prepare manageable pieces of text for embedding and retrieval.
- Retain document or page metadata where supported by the implementation.
- Make it possible to retrieve a relevant portion of a document instead of passing all extracted text to the LLM.

Chunk size and overlap affect retrieval quality: very small chunks can lose context, while very large chunks may contain unrelated information. The appropriate settings depend on the document type and use case.

### Semantic Embeddings

- Use Sentence Transformers to convert text into numerical vectors.
- Represent document chunks in a form suitable for similarity search.
- Embed a user question so it can be compared with document content.

Embeddings capture aspects of semantic similarity. They can help retrieve passages that express a similar idea even when they do not use exactly the same words.

### FAISS Vector Search

- Index document embeddings using FAISS.
- Search for chunks that are semantically relevant to a user's question.
- Supply retrieved passages to the RAG pipeline as context.

FAISS is used for vector similarity search. It is not the language model and does not generate answers by itself.

### Local LLM Integration

- Use Ollama to run a language model locally.
- Use the `llama3.2:3b` model in the current development setup.
- Pass the user's question and retrieved document context to the model.
- Return the generated response to the frontend.

Local inference can reduce reliance on hosted LLM APIs. Actual privacy characteristics also depend on application logging, file handling, operating-system security, and any external services used elsewhere in the application.

### FastAPI Backend

- Expose HTTP endpoints for document upload and question answering.
- Connect document processing, retrieval, and LLM generation.
- Validate incoming requests using the application's request models where configured.
- Return results to the browser frontend.

Consult the live API documentation at `/docs` when the backend is running to inspect the endpoints currently exposed by the code.

### Browser-Based Frontend

- Provide a PDF upload interface.
- Let users enter questions about the document.
- Send requests to the backend API.
- Display the submitted question and generated answer in the conversation area.

The frontend uses HTML, CSS, and JavaScript rather than React.

## System Architecture

The application separates the browser interface from the backend services. The frontend sends HTTP requests to FastAPI. The backend coordinates PDF extraction, chunking, embedding generation, vector search, and communication with Ollama.

```text
┌──────────────────────────────────────────────┐
│                Browser Frontend              │
│                                              │
│  HTML + CSS + JavaScript                     │
│  • PDF upload                                │
│  • Question input                            │
│  • Answer display                            │
└──────────────────────┬───────────────────────┘
                       │ HTTP / JSON / File Upload
                       ▼
┌──────────────────────────────────────────────┐
│                FastAPI Backend               │
│                                              │
│  • API endpoints                             │
│  • Request validation                        │
│  • Document workflow orchestration           │
│  • RAG question-answering workflow           │
└──────────────┬─────────────────────┬─────────┘
               │                     │
               ▼                     ▼
┌────────────────────────┐  ┌────────────────────────┐
│ Document Processing    │  │ Retrieval and Indexing │
│                        │  │                        │
│ • PyMuPDF extraction   │  │ • Sentence Transformers│
│ • Text chunking        │  │ • Embeddings           │
│ • Page/content analysis│  │ • FAISS vector search  │
│ • Structured extraction│  │ • Relevant chunk search│
│   where implemented    │  │                        │
└────────────┬───────────┘  └────────────┬───────────┘
             │                           │
             └─────────────┬─────────────┘
                           ▼
             ┌──────────────────────────┐
             │       RAG Service        │
             │                          │
             │ Question + Retrieved     │
             │ Document Context         │
             └────────────┬─────────────┘
                          │ Prompt / Context
                          ▼
             ┌──────────────────────────┐
             │       Ollama Runtime     │
             │       llama3.2:3b        │
             └────────────┬─────────────┘
                          │ Generated response
                          ▼
             ┌──────────────────────────┐
             │ FastAPI Response         │
             └────────────┬─────────────┘
                          ▼
                  Browser Answer UI
```

The diagram describes the intended service relationships. Exact service boundaries and any persistent storage behavior should be checked against the current implementation.

## Data Flow

### 1. PDF Upload and Extraction

```text
User selects a PDF
       |
       v
Browser frontend
       |
       v
FastAPI upload endpoint
       |
       v
PyMuPDF text extraction
       |
       v
Extracted page text
```

The backend receives the PDF and extracts its text. Extraction quality depends on the PDF's structure, whether text is selectable, and whether the document uses complex layouts or tables.

### 2. Chunking and Indexing

```text
Extracted document text
       |
       v
Text chunking
       |
       v
Sentence Transformers
       |
       v
Chunk embedding vectors
       |
       v
FAISS index
       |
       v
Searchable document chunks
```

Chunking divides the document into smaller units. The embedding model converts each chunk into a vector, and FAISS makes those vectors searchable by similarity.

### 3. Question Answering

```text
User enters a question
       |
       v
Frontend sends request to FastAPI
       |
       v
Question embedding
       |
       v
FAISS retrieves relevant chunks
       |
       v
RAG service builds context for the LLM
       |
       v
Ollama runs llama3.2:3b
       |
       v
Generated answer returned by FastAPI
       |
       v
Frontend displays question and answer
```

The retrieval step is important because it supplies document-specific context to the model. The model then uses that context to formulate a response. Retrieval can still miss relevant passages, and a language model can still generate unsupported information.

### 4. Document Structure and Advanced Extraction

The repository includes additional document-processing modules for analysis, geometry-based table detection, logical-record reconstruction, and table-record extraction. These modules are intended to support more structured document interpretation beyond basic text extraction.

Their exact role in the active request pipeline—and whether each is currently invoked by the upload or question-answering endpoints—should be verified in the code before describing them as production-ready features.

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Programming language | Python | Backend logic and document-processing pipeline |
| Backend framework | FastAPI | HTTP API and request handling |
| PDF processing | PyMuPDF | Extract text from PDF documents |
| Text embeddings | Sentence Transformers | Convert document chunks and questions into vectors |
| Vector search | FAISS | Index and retrieve semantically similar vectors |
| Local LLM runtime | Ollama | Run a language model locally |
| Language model | `llama3.2:3b` | Generate responses using retrieved context |
| Frontend | HTML | Structure the browser interface |
| Frontend styling | CSS | Layout, visual design, and responsive styling |
| Frontend behavior | JavaScript | Upload files, send questions, and render answers |
| Testing | Python testing tools in `tests/`, if configured | Validate extraction and application behavior |
| Version control | Git and GitHub | Track code changes and maintain the repository |

Package versions should be taken from the project's actual dependency files rather than guessed in this document.

## Project Structure

The repository contains the following known application areas. The tree below summarizes the main files and service modules currently reported in the project; update it if your local structure differs.

```text
AI-Document-Assistant/
├── backend/
│   ├── main.py
│   ├── models/
│   │   ├── request_models.py
│   │   └── document_models.py
│   └── services/
│       ├── chunking_service.py
│       ├── document_service.py
│       ├── indexing_service.py
│       ├── llm_service.py
│       ├── rag_service.py
│       ├── document_analyzer.py
│       ├── geometry_table_detector.py
│       ├── logical_record_pipeline.py
│       ├── logical_record_reconstructor.py
│       ├── page_analyzer.py
│       └── table_record_extractor.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/
├── AI-Document-Assistant.code-workspace
└── README.md
```

A dependency file such as `requirements.txt` should be listed here once its exact location has been confirmed. Generated indexes, uploaded documents, virtual environments, and local model files should not be documented as committed assets unless they are intentionally part of the repository.

### Backend

The `backend/` directory contains the FastAPI entry point, request/document models, and service modules responsible for processing and answering questions.

- `main.py` — application entry point and API routes.
- `models/request_models.py` — request schemas used by the API, according to the current project structure.
- `models/document_models.py` — document-related structures such as pages, blocks, tables, and chunks, if used by the active pipeline.
- `services/document_service.py` — PDF text extraction and document handling.
- `services/chunking_service.py` — splits extracted content into chunks.
- `services/indexing_service.py` — prepares and searches the vector index.
- `services/rag_service.py` — coordinates retrieval and response generation.
- `services/llm_service.py` — communicates with the local language model.
- Additional analyzer and table modules — support document layout analysis and structured extraction where integrated.

These descriptions summarize intended responsibilities; the implementation in each file is the source of truth.

### Frontend

The `frontend/` directory contains the browser-based user interface.

- `index.html` — page structure.
- `style.css` — visual styling and layout.
- `script.js` — user interactions and API calls.

The frontend communicates with the backend over HTTP. If the API address is configured directly in JavaScript, the frontend must use an address that matches the backend environment.

### Tests

The `tests/` directory is intended to hold automated checks for document extraction and related behavior. Run only the test commands supported by the test files and installed dependencies; test coverage should not be inferred from the existence of the directory alone.

## RAG Pipeline Explained

Retrieval-Augmented Generation combines a retrieval system with a language model.

### Retrieval

The application prepares document content as chunks, creates embeddings, and uses FAISS to find chunks that are semantically similar to the user's question.

### Augmentation

The retrieved text is supplied to the language model as context alongside the question. This gives the model relevant document content to use when constructing its response.

### Generation

Ollama runs the configured local model, `llama3.2:3b`, and returns a generated answer. The quality of that answer depends on the document text, chunking strategy, retrieval quality, prompt design, and model behavior.

### Why RAG?

RAG is useful for document question answering because it can:

- Ground answers in content retrieved from a user's documents.
- Search documents without requiring the entire document to fit into every prompt.
- Separate retrieval from answer generation, making each part easier to inspect and improve.
- Allow the document index to be updated as new content is processed.

RAG does not automatically guarantee factual correctness. A reliable implementation should provide useful source references, evaluate retrieval quality, and communicate when the document does not contain enough evidence to answer.

## Local LLM Integration

The current development setup uses Ollama with `llama3.2:3b`.

Ollama manages local model execution, while the backend's LLM service is responsible for sending the prompt or request and handling the response. The RAG service provides the retrieved document context used for question answering.

### Benefits

- Reduces reliance on a hosted model API.
- Allows experimentation without configuring a paid LLM API key.
- Keeps inference on the local machine when the Ollama runtime and application are configured locally.

### Considerations

- Model downloads require disk space.
- Inference speed depends on available memory and hardware.
- Smaller models may struggle with complex reasoning or long context.
- Local inference does not remove the need to protect uploaded files, logs, and system access.

## Setup and Installation

The commands below reflect the known local development workflow. Confirm the repository's dependency-file location and installed package versions before relying on them on a clean machine.

### Prerequisites

- Git
- Python compatible with the project's installed dependencies
- Ollama
- The `llama3.2:3b` model downloaded through Ollama
- A modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/nikhithabhandary08/AI-Document-Assistant.git
cd AI-Document-Assistant
```

### 2. Create a Virtual Environment

From the repository root in Windows Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

If your environment already has a virtual environment, activate that environment instead of creating another one.

### 3. Install Backend Dependencies

Use the dependency file that actually exists in the repository. If `requirements.txt` is at the root:

```bash
pip install -r requirements.txt
```

If the project does not currently contain a complete dependency file, install the dependencies specified by the implementation and create a reproducible requirements file before publishing setup instructions. Do not assume a root-level `requirements.txt` exists.

### 4. Install and Prepare Ollama

Install Ollama using its official installation instructions, then download the model:

```bash
ollama pull llama3.2:3b
```

Confirm the model is available:

```bash
ollama list
```

Make sure Ollama is running before trying the question-answering workflow.

### 5. Start the FastAPI Backend

From the repository root, with the correct Python environment activated:

```bash
python -m uvicorn backend.main:app --reload
```

If the application starts successfully, the API is typically available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

If the command fails, check the actual import path, dependency installation, and terminal working directory rather than changing the code blindly.

### 6. Start the Frontend

Open a second terminal and serve the frontend directory:

```bash
cd frontend
python -m http.server 5500
```

Open the interface in a browser:

```text
http://127.0.0.1:5500/
```

Keep the frontend and backend terminals running while using the application. The frontend API URL must point to the running backend.

### 7. Try the Application

1. Open the frontend in the browser.
2. Upload a PDF that contains selectable text.
3. Wait for the upload and processing request to complete.
4. Enter a question that can be answered from the PDF.
5. Submit the question.
6. Review the generated answer and verify important details against the original document.

## API Overview

The frontend currently uses the document upload and question-answering routes described in the local application workflow.

| Operation | Route | Purpose |
|---|---|---|
| Upload a document | `POST /documents/upload` | Submit a PDF for processing |
| Ask a question | `POST /ask` | Submit a question and receive a response |

Confirm the exact request fields, response schemas, status codes, and whether additional routes exist by opening `http://127.0.0.1:8000/docs` while the backend is running. This table describes the known frontend workflow and is not a replacement for the live API specification.

## Testing and Validation

Testing should cover the complete flow rather than only checking whether the application starts.

### Document Extraction

- Test a text-based PDF with a few pages.
- Check that extracted text is readable and in the expected order.
- Test a PDF with unusual formatting or tables.
- Confirm that empty or unsupported files return understandable errors.

### Chunking and Embeddings

- Confirm extracted content is divided into non-empty chunks.
- Check that chunk metadata remains associated with the correct document or page where implemented.
- Confirm embedding dimensions and vector counts are consistent.
- Verify that the FAISS index contains the expected number of vectors.

### Retrieval and Question Answering

- Ask a question whose answer is clearly present in the document.
- Ask a question about a different section of the document.
- Ask a question whose answer is not present and observe whether the system avoids unsupported claims.
- Check behavior when no relevant chunks are retrieved.
- Confirm the LLM service handles Ollama errors or unavailable models clearly.

### Frontend and API

- Verify that a PDF upload reaches the backend.
- Verify that question requests use the expected request format.
- Confirm the question and answer appear in the interface.
- Test invalid uploads and API failures.
- Confirm the frontend displays a useful error if the backend is unavailable.

Run the automated tests in `tests/` using the test runner and configuration actually present in the repository. Do not claim all tests pass until they have been executed successfully.

## Limitations

- Text extraction quality depends on the PDF structure and whether text is embedded in the file.
- Scanned PDFs may need OCR if OCR is not already implemented.
- Tables, multi-column layouts, headers, footers, and reading order can be difficult to reconstruct accurately.
- Chunk size and overlap can affect retrieval quality.
- Semantic similarity does not always identify the exact passage needed.
- The LLM may generate incorrect or unsupported answers even when relevant context is supplied.
- Local inference performance depends on the machine running Ollama.
- The current frontend is configured for local development and may require changes for deployment, including API URL configuration and CORS settings.

## Future Improvements

- Add source citations and page numbers to answers.
- Improve table extraction and preservation of document layout.
- Add OCR support for scanned PDFs if needed.
- Support multiple documents and document selection.
- Add configurable chunking and retrieval parameters.
- Evaluate retrieval using a small set of representative questions and expected source passages.
- Add automated tests for extraction, chunking, indexing, and API behavior.
- Improve logging and error messages without exposing sensitive document content.
- Add upload limits, file validation, and safer temporary-file handling.
- Add configuration through environment variables where appropriate.
- Improve frontend/backend configuration for deployment.
- Add a clear indication when retrieved evidence is insufficient to answer a question.

## Security and Privacy Notes

- Do not commit API keys, credentials, personal documents, or private environment files.
- Review `.gitignore` before pushing changes.
- Treat uploaded PDFs as potentially sensitive.
- Avoid logging full document contents or user questions unless necessary and appropriately protected.
- Local model inference can reduce external data transfer, but it does not by itself guarantee complete application privacy or security.

## Learning Outcomes

This project explores practical skills in:

- Building HTTP APIs with FastAPI.
- Extracting content from PDFs with PyMuPDF.
- Splitting documents into retrievable chunks.
- Generating text embeddings with Sentence Transformers.
- Performing vector similarity search with FAISS.
- Designing a Retrieval-Augmented Generation pipeline.
- Integrating a locally executed LLM through Ollama.
- Connecting a browser frontend to an AI backend.
- Separating application responsibilities into service modules.
- Testing a document-processing and question-answering workflow.

## Author

**Nikhitha Bhandary**

GitHub: [nikhithabhandary08](https://github.com/nikhithabhandary08)

Repository: [AI-Document-Assistant](https://github.com/nikhithabhandary08/AI-Document-Assistant)

---

*Built as a learning project to explore document processing, semantic retrieval, and local LLM-powered question answering.*
