from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_base.models.base import Base

SessionLocal = None
Engine = None


def init_db(db_url: str):
    global SessionLocal, Engine

    Engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(Engine)
    SessionLocal = sessionmaker(bind=Engine, expire_on_commit=False)


@contextmanager
def get_session():
    session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()