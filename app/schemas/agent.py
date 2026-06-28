from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AgentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    tenant_id: str = Field(min_length=1, max_length=100)
    runtime: str = Field(default="python", min_length=1, max_length=100)
    config: dict[str, Any] | None = None


class AgentRead(BaseModel):
    id: int
    user_id: str
    name: str
    tenant_id: str
    runtime: str
    status: str
    config: dict[str, Any] | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentPage(BaseModel):
    items: list[AgentRead]
    next_cursor: int | None = None


class AgentAction(BaseModel):
    action: str
