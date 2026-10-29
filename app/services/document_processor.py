
from pathlib import Path

import fitz  # PyMuPDF
from docx import Document


def extract_text(file_path: str) -> str:
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        with fitz.open(path) as pdf:
            text = "\n".join(page.get_text() for page in pdf)

    elif extension == ".docx":
        document = Document(path)
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)

    elif extension == ".txt":
        text = path.read_text(encoding="utf-8", errors="replace")

    else:
        raise ValueError("Unsupported document format.")

    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

    if not text:
        raise ValueError(
            "No readable text found. The PDF may be scanned or the document may be empty."
        )

    return text
