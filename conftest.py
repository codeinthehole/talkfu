import os
import tempfile

import pytest
from sqlalchemy.orm import clear_mappers, sessionmaker

import database
import interface
import orm


@pytest.fixture
def session(bind_orm, test_db_url):
    """
    Inject a DB session object.

    Each session will have its own database with the schema created.
    """
    engine = database.get_engine(test_db_url)

    # Create DB schema.
    database.create_schema(test_db_url)

    yield sessionmaker(bind=engine)()


@pytest.fixture
def bind_orm():
    # Register mapping between ORM objects and domain models.
    orm.register_mappers()

    yield

    # Unregister mapping between ORM objects and domain models.
    clear_mappers()


@pytest.fixture
def test_db_url():
    # Create a temporary database location.
    db_fd, db_path = tempfile.mkstemp()

    yield f"sqlite:///{db_path}"

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def flask_app(bind_orm, test_db_url):
    app = interface.create_app(
        # Use in-memory database.
        config=dict(
            # This ensures exceptions are propagated rather than handled by the app's error handlers
            # https://flask.palletsprojects.com/en/2.3.x/config/#TESTING
            TESTING=True,
            # Pass in the test database URL.
            DB_URL=test_db_url,
        ),
    )
    yield app


@pytest.fixture
def client(flask_app):
    return flask_app.test_client()
