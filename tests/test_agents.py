from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_agent() -> None:
    payload = {
        "name": "billing-reconciler",
        "tenant_id": "tenant-123",
        "runtime": "python",
        "config": {"model": "gpt-4o-mini"},
    }

    response = client.post("/v1/agents/", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["name"] == payload["name"]
    assert body["tenant_id"] == payload["tenant_id"]
    assert body["runtime"] == payload["runtime"]
    assert body["status"] == "created"
    assert body["config"] == payload["config"]
    assert "created_at" in body
