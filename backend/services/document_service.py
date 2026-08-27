import pymupdf


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from all pages of a PDF file."""

    text = ""

    with pymupdf.open(file_path) as document:
        for page in document:
            text += page.get_text()

    return text