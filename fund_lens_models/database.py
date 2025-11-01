from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_engine(database_url: str):
    """Create SQLAlchemy engine."""
    return create_engine(database_url, pool_pre_ping=True)


def get_session_factory(database_url: str):
    """Create session factory."""
    engine = get_engine(database_url)
    return sessionmaker(bind=engine)


def get_session(database_url: str) -> Generator[Session, None, None]:
    """Dependency for FastAPI/etc."""
    sessionlocal = get_session_factory(database_url)
    session = sessionlocal()
    try:
        yield session
    finally:
        session.close()
