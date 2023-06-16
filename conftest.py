import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from orm import mapper_registry, register_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")

    # Create tables.
    mapper_registry.metadata.create_all(engine)

    return engine


@pytest.fixture
def session_factory(in_memory_db):
    # Register mapping between ORM objects and domain models.
    register_mappers()
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def session(session_factory):
    return session_factory()
