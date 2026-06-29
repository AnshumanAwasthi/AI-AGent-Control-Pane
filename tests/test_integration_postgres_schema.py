from pathlib import Path

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.config import settings
from app.db import SessionLocal, database_url
from app.main import app


client = TestClient(app)


def _auth_headers(user_id: str = "integration-user") -> dict[str, str]:
    token = jwt.encode({"user_id": user_id}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.skipif(not database_url.startswith("postgresql+psycopg://"), reason="PostgreSQL-only integration test")
def test_postgres_schema_enum_works_for_create_agent() -> None:
    script_path = Path(__file__).resolve().parents[1] / "sql" / "001_create_agents_table.sql"
    script_sql = script_path.read_text(encoding="utf-8")

    with SessionLocal() as db:
        db.execute(text("DROP TABLE IF EXISTS agents CASCADE;"))
        db.execute(text("DROP TYPE IF EXISTS agent_status_type CASCADE;"))
        db.commit()

        db.execute(text(script_sql))
        db.commit()

    response = client.post(
        "/v1/agents/",
        json={
            "name": "integration-schema-agent",
            "tenant_id": "tenant-integration",
            "runtime": "python",
            "config": {"model": "gpt-4o-mini"},
        },
        headers=_auth_headers(),
    )

    assert response.status_code == 201
    assert response.json()["status"] == "created"
