from sqlalchemy import DateTime, Enum as SQLEnum, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.agent_status import AgentStatusType
from app.core.config import settings
from app.db import Base


class Agent(Base):
    __tablename__ = settings.agents_table_name

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    runtime: Mapped[str] = mapped_column(String(100), nullable=False, default="python")
    status: Mapped[str] = mapped_column(
        SQLEnum(
            *(status.value for status in AgentStatusType),
            name="agent_status_type",
            native_enum=True,
            validate_strings=True,
        ),
        nullable=False,
        default=AgentStatusType.CREATED.value,
    )
    config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
