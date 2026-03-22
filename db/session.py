"""
Database engine, session factory, and session context manager.

This module is the single point of contact between the application
and the database connection layer. All services obtain their database
session exclusively through get_session() — never by importing the
engine or SessionLocal directly.

The session is configured with autocommit=False and autoflush=False
so that all changes are explicit and transactional. Commits happen
automatically on clean exit from the context manager. Any exception
triggers a rollback before the error is re-raised.
"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import settings


engine = create_engine(settings.database_url, echo=False)
"""SQLAlchemy engine bound to the DATABASE_URL from .env.

echo=False suppresses SQL logging in production. Set to True
temporarily during development if you want to inspect the raw
queries being generated.
"""

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
"""Session factory — call SessionLocal() to get a new session instance.

Not used directly outside this module. All code should use get_session().
"""


@contextmanager
def get_session() -> Session:
    """Provide a transactional database session as a context manager.

    Yields a SQLAlchemy Session that automatically commits on clean exit
    and rolls back on any exception. The session is always closed in the
    finally block regardless of outcome.

    Usage:
        with get_session() as session:
            client = session.get(Client, client_id)

    Yields:
        Session: An active SQLAlchemy ORM session.

    Raises:
        Any exception raised inside the with block is re-raised after
        the session has been rolled back and closed.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
