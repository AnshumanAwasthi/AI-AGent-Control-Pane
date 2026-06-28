from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id, get_db
from app.models import Agent
from app.schemas.agent import AgentCreate, AgentRead


router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
def create_agent(
    payload: AgentCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> Agent:
    agent = Agent(
        user_id=user_id,
        name=payload.name,
        tenant_id=payload.tenant_id,
        runtime=payload.runtime,
        status="created",
        config=payload.config,
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent
