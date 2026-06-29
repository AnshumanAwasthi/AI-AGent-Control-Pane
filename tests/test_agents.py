import jwt
from uuid import uuid4
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


def test_list_agents_with_cursor_pagination() -> None:
    user_id = "paging-user"
    headers = _auth_headers(user_id)

    for idx in range(3):
        payload = {
            "name": f"agent-{idx}",
            "tenant_id": "tenant-pagination",
            "runtime": "python",
            "config": {"model": "gpt-4o-mini", "idx": idx},
        }
        create_response = client.post("/v1/agents/", json=payload, headers=headers)
        assert create_response.status_code == 201

    first_page = client.get("/v1/agents/?limit=2", headers=headers)
    assert first_page.status_code == 200
    first_body = first_page.json()
    assert len(first_body["items"]) == 2
    assert first_body["next_cursor"] is not None
    assert all(item["user_id"] == user_id for item in first_body["items"])

    second_page = client.get(f"/v1/agents/?limit=2&cursor={first_body['next_cursor']}", headers=headers)
    assert second_page.status_code == 200
    second_body = second_page.json()
    assert len(second_body["items"]) >= 1
    assert all(item["user_id"] == user_id for item in second_body["items"])


def test_list_agents_requires_bearer_token() -> None:
    response = client.get("/v1/agents/")
    assert response.status_code == 401


def test_list_agents_without_trailing_slash_works() -> None:
    headers = _auth_headers("slashless-user")
    response = client.get("/v1/agents", headers=headers, follow_redirects=False)
    assert response.status_code == 200


def test_get_agent_by_id() -> None:
    payload = {
        "name": "get-by-id-agent",
        "tenant_id": "tenant-123",
        "runtime": "python",
        "config": {"model": "gpt-4o-mini"},
    }
    headers = _auth_headers("owner-user")
    create_response = client.post("/v1/agents/", json=payload, headers=headers)
    assert create_response.status_code == 201
    created = create_response.json()

    get_response = client.get(f"/v1/agents/{created['id']}", headers=headers)
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["id"] == created["id"]
    assert fetched["user_id"] == "owner-user"
    assert fetched["name"] == payload["name"]


def test_get_agent_by_id_returns_404_for_other_user() -> None:
    payload = {
        "name": "private-agent",
        "tenant_id": "tenant-xyz",
        "runtime": "python",
        "config": {"model": "gpt-4o-mini"},
    }
    create_response = client.post("/v1/agents/", json=payload, headers=_auth_headers("owner-only"))
    assert create_response.status_code == 201
    created = create_response.json()

    other_user_response = client.get(f"/v1/agents/{created['id']}", headers=_auth_headers("other-user"))
    assert other_user_response.status_code == 404


def test_agent_actions_update_status() -> None:
    headers = _auth_headers("action-user")
    payload = {
        "name": "action-agent",
        "tenant_id": "tenant-actions",
        "runtime": "python",
        "config": {"model": "gpt-4o-mini"},
    }
    create_response = client.post("/v1/agents/", json=payload, headers=headers)
    assert create_response.status_code == 201
    agent_id = create_response.json()["id"]

    cases = [
        ("start", "running"),
        ("pause", "paused"),
        ("resume", "running"),
        ("stop", "stopped"),
    ]
    for action, expected_status in cases:
        response = client.post(f"/v1/agents/{agent_id}/actions", json={"action": action}, headers=headers)
        assert response.status_code == 200
        assert response.json()["status"] == expected_status


def test_agent_actions_returns_404_for_other_user() -> None:
    owner_headers = _auth_headers("owner-actions")
    payload = {
        "name": "private-action-agent",
        "tenant_id": "tenant-actions",
        "runtime": "python",
        "config": {"model": "gpt-4o-mini"},
    }
    create_response = client.post("/v1/agents/", json=payload, headers=owner_headers)
    assert create_response.status_code == 201
    agent_id = create_response.json()["id"]

    other_response = client.post(
        f"/v1/agents/{agent_id}/actions",
        json={"action": "start"},
        headers=_auth_headers("different-user"),
    )
    assert other_response.status_code == 404


def test_agent_actions_returns_400_for_invalid_action() -> None:
    headers = _auth_headers("invalid-action-user")
    payload = {
        "name": "invalid-action-agent",
        "tenant_id": "tenant-actions",
        "runtime": "python",
        "config": {"model": "gpt-4o-mini"},
    }
    create_response = client.post("/v1/agents/", json=payload, headers=headers)
    assert create_response.status_code == 201
    agent_id = create_response.json()["id"]

    invalid_response = client.post(
        f"/v1/agents/{agent_id}/actions",
        json={"action": "restart"},
        headers=headers,
    )
    assert invalid_response.status_code == 400
    assert "Invalid action 'restart'" in invalid_response.json()["detail"]


def test_agent_actions_reject_invalid_transition() -> None:
    headers = _auth_headers("transition-user")
    payload = {
        "name": "transition-agent",
        "tenant_id": "tenant-actions",
        "runtime": "python",
        "config": {"model": "gpt-4o-mini"},
    }
    create_response = client.post("/v1/agents/", json=payload, headers=headers)
    assert create_response.status_code == 201
    agent_id = create_response.json()["id"]

    first_response = client.post(
        f"/v1/agents/{agent_id}/actions",
        json={"action": "start"},
        headers=headers,
    )
    assert first_response.status_code == 200

    second_response = client.post(
        f"/v1/agents/{agent_id}/actions",
        json={"action": "stop"},
        headers=headers,
    )
    assert second_response.status_code == 200

    invalid_transition_response = client.post(
        f"/v1/agents/{agent_id}/actions",
        json={"action": "pause"},
        headers=headers,
    )
    assert invalid_transition_response.status_code == 409
    assert "is not allowed when agent status is 'stopped'" in invalid_transition_response.json()["detail"]
    assert "transition to 'paused'" in invalid_transition_response.json()["detail"]


def test_create_agent_enforces_tenant_quota() -> None:
    original_quota = settings.tenant_max_agents
    settings.tenant_max_agents = 1
    try:
        tenant_id = f"tenant-quota-test-{uuid4()}"

        first_payload = {
            "name": "quota-agent-1",
            "tenant_id": tenant_id,
            "runtime": "python",
            "config": {"model": "gpt-4o-mini"},
        }
        first_response = client.post("/v1/agents/", json=first_payload, headers=_auth_headers("quota-user-1"))
        assert first_response.status_code == 201

        second_payload = {
            "name": "quota-agent-2",
            "tenant_id": tenant_id,
            "runtime": "python",
            "config": {"model": "gpt-4o-mini"},
        }
        second_response = client.post("/v1/agents/", json=second_payload, headers=_auth_headers("quota-user-2"))

        assert second_response.status_code == 403
        assert "reached the agent quota" in second_response.json()["detail"]
    finally:
        settings.tenant_max_agents = original_quota
