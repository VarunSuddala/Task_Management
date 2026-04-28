from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_engine():
    return engine


def get_session_local():
    return SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
