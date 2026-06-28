from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id, get_db
from app.models import Agent
from app.schemas.agent import AgentCreate, AgentPage, AgentRead


router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/{agentid}", response_model=AgentRead)
def get_agent(
    agentid: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> Agent:
    query = select(Agent).where(Agent.id == agentid, Agent.user_id == user_id)
    agent = db.scalars(query).first()
    if agent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agent


@router.get("/", response_model=AgentPage)
def list_agents(
    cursor: int | None = Query(default=None, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> AgentPage:
    query = select(Agent).where(Agent.user_id == user_id)
    if cursor is not None:
        query = query.where(Agent.id > cursor)

    query = query.order_by(Agent.id.asc()).limit(limit + 1)
    records = list(db.scalars(query).all())

    has_more = len(records) > limit
    items = records[:limit]
    next_cursor = items[-1].id if has_more and items else None

    return AgentPage(items=items, next_cursor=next_cursor)


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
