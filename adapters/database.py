from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from adapters.orm import mapper_registry


def get_session(db_url: str) -> Session:
    return sessionmaker(bind=get_engine(db_url))()


def get_engine(db_url: str) -> Engine:
    return create_engine(db_url)


def create_schema(db_url: str) -> None:
    engine = get_engine(db_url)
    if len(mapper_registry.mappers) == 0:
        raise RuntimeError(
            "No model mappings found. Did you forget to register mappers?"
        )
    mapper_registry.metadata.create_all(engine)
