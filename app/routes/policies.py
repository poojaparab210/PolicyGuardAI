
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.policy_qa import index_uploaded_policy
from app.services.document_processor import extract_text

router = APIRouter(prefix="/policies", tags=["Policies"])

UPLOAD_DIR = Path("data/uploads")
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/upload")
async def upload_policy(file: UploadFile = File(...)):
    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are supported.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(status_code=400, detail="The file is empty.")

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB.",
        )

    policy_id = str(uuid4())
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    safe_filename = f"{policy_id}{extension}"
    destination = UPLOAD_DIR / safe_filename

    destination.write_bytes(content)

    try:
        text = extract_text(str(destination))
        chunk_count = index_uploaded_policy(policy_id, str(destination))
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=422,
            detail="Could not process and index the uploaded policy.",
        ) from exc

    return {
        "message": "Policy uploaded successfully.",
        "policy_id": policy_id,
        "filename": file.filename,
        "stored_as": safe_filename,
        "size_bytes": len(content),
        "status": "uploaded",
        "indexed_chunks": chunk_count,
        "characters_extracted": len(text),
    }
