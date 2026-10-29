
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_missing_policy_returns_404():
    response = client.get(
        "/policies/nonexistent-policy-id/text"
    )

    assert response.status_code == 404


def test_empty_question_is_rejected():
    response = client.post(
        "/policies/nonexistent-policy-id/ask",
        json={"question": ""}
    )

    assert response.status_code == 422
