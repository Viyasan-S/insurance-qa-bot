
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ask_rejects_missing_api_key():
    response = client.post(
        "/ask",
        json={"question": "What is the accidental death benefit?"},
    )

    assert response.status_code == 401


def test_ask_rejects_invalid_api_key(monkeypatch):
    monkeypatch.setenv("API_KEY", "correct-test-key")

    response = client.post(
        "/ask",
        json={"question": "What is the accidental death benefit?"},
        headers={"X-API-Key": "wrong-key"},
    )

    assert response.status_code == 401


def test_ask_rejects_short_question(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")

    response = client.post(
        "/ask",
        json={"question": "hi"},
        headers={"X-API-Key": "test-key"},
    )

    assert response.status_code == 422
