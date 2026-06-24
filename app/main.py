from fastapi import FastAPI

from app.api.v1.routes.agents import router as agents_router
from app.api.v1.routes.health import router as health_router
from app.core.config import settings
from app.db import Base, engine
import app.models  # noqa: F401


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="0.1.0",
)

app.include_router(health_router, prefix=settings.api_v1_prefix)
app.include_router(agents_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"message": f"Welcome to {settings.app_name}"}
