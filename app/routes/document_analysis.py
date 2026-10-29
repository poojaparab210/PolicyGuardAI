
from pathlib import Path

from pydantic import BaseModel, Field

from fastapi import APIRouter, HTTPException

from app.services.document_processor import extract_text

from app.services.policy_qa import (
    index_uploaded_policy,
    ask_policy_question,
)

router = APIRouter(prefix="/policies", tags=["Document Analysis"])

UPLOAD_DIR = Path("data/uploads")


@router.get("/{policy_id}/text")
def get_policy_text(policy_id: str):
    matches = [
        path
        for path in UPLOAD_DIR.glob(f"{policy_id}.*")
        if path.is_file()
    ]

    if not matches:
        raise HTTPException(status_code=404, detail="Policy not found.")

    try:
        text = extract_text(str(matches[0]))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail="Could not read this document.",
        ) from exc

    return {
        "policy_id": policy_id,
        "characters": len(text),
        "text": text,
    }

class PolicyQuestion(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question about the uploaded policy",
    )


@router.post("/{policy_id}/ask")
def ask_policy(policy_id: str, payload: PolicyQuestion):
    try:
        return ask_policy_question(
            policy_id=policy_id,
            question=payload.question,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
