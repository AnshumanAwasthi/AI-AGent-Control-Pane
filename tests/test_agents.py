import jwt
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


client = TestClient(app)


def _auth_headers(user_id: str = "user-123") -> dict[str, str]:
    token = jwt.encode({"user_id": user_id}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return {"Authorization": f"Bearer {token}"}


def test_create_agent() -> None:
    payload = {
        "name": "billing-reconciler",
        "tenant_id": "tenant-123",
        "runtime": "python",
        "config": {"model": "gpt-4o-mini"},
    }

    response = client.post("/v1/agents/", json=payload, headers=_auth_headers("user-42"))

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["user_id"] == "user-42"
    assert body["name"] == payload["name"]
    assert body["tenant_id"] == payload["tenant_id"]
    assert body["runtime"] == payload["runtime"]
    assert body["status"] == "created"
    assert body["config"] == payload["config"]
    assert "created_at" in body


def test_create_agent_requires_bearer_token() -> None:
    payload = {
        "name": "billing-reconciler",
        "tenant_id": "tenant-123",
        "runtime": "python",
        "config": {"model": "gpt-4o-mini"},
    }

    response = client.post("/v1/agents/", json=payload)
    assert response.status_code == 401
