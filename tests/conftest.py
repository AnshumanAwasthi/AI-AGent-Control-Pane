import app.models  # noqa: F401
from app.db import Base, engine


def pytest_sessionstart(session) -> None:  # type: ignore[no-untyped-def]
    Base.metadata.create_all(bind=engine)
