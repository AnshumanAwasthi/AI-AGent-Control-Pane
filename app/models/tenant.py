from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings
from app.db import Base


class Tenant(Base):
    __tablename__ = settings.tenant_table_name

    tenant_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    max_agents: Mapped[int] = mapped_column(nullable=False, default=0)
    max_running_agents: Mapped[int] = mapped_column(nullable=False, default=0)
