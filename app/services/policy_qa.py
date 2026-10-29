
from app.services.document_processor import extract_text
from app.services.retrieval import index_policy, search_policy
from app.services.llm_service import answer_policy_question


def index_uploaded_policy(policy_id: str, file_path: str) -> int:
    """Extract and index an uploaded policy document."""
    text = extract_text(file_path)
    return index_policy(policy_id, text)


def ask_policy_question(policy_id: str, question: str) -> dict:
    """Retrieve relevant policy passages and answer a question."""
    results = search_policy(
        policy_id=policy_id,
        question=question,
        top_k=3,
    )

    if not results or results[0]["distance"] > 0.50:
        return {
            "policy_id": policy_id,
            "question": question,
            "answer": (
                "I couldn't find relevant information in the "
                "indexed policy. Please check the document or "
                "ask a more specific question."
            ),
            "sources": [],
        }

    context = "\n\n".join(item["text"] for item in results)

    answer = answer_policy_question(
        question=question,
        context=context,
    )

    return {
        "policy_id": policy_id,
        "question": question,
        "answer": answer,
        "sources": [
            {
                "chunk_index": item["chunk_index"],
                "distance": item["distance"],
                "text": item["text"],
            }
            for item in results
        ],
    }
