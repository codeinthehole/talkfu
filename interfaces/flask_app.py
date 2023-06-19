"""
Interface layer

A thin layer, responsible for translating HTTP requests into calls into the usecase layer.
"""
import datetime
from typing import Any

import flask
from adapters import database, orm, repository
from usecases import usecases


def add_talk() -> tuple[str, int]:
    # Get a DB session.
    session = database.get_session(flask.current_app.config["DB_URL"])

    # Set-up repository.
    repo = repository.SqlAlchemyTalkRepository(session)

    usecases.add_talk(
        ref=flask.request.json["ref"],
        title=flask.request.json["title"],
        description=flask.request.json["description"],
        event_date=datetime.datetime.strptime(
            flask.request.json["event_date"], "%Y-%m-%d"
        ).date(),
        repository=repo,
        session=session,
    )

    return "", 201


def vote() -> tuple[str, int]:
    # Get a DB session.
    session = database.get_session(flask.current_app.config["DB_URL"])

    # Set-up repository.
    repo = repository.SqlAlchemyTalkRepository(session)

    try:
        usecases.vote_on_talk(
            talk_ref=flask.request.json["talk_ref"],
            username=flask.request.json["username"],
            num_followers=flask.request.json["num_followers"],
            repository=repo,
            session=session,
        )
    except usecases.TalkDoesNotExist:
        return "", 404

    return "", 201


def create_app(config: dict[str, Any] | None = None) -> flask.Flask:
    """
    Return a configured Flask application.
    """
    app = flask.Flask(__name__)

    if config is not None:
        # Use passed in config, if passed.
        app.config.from_mapping(config)
    else:
        # Load from file.
        app.config.from_pyfile("config.py", silent=False)

    # Register routes.
    app.route("/vote", methods=["POST"])(vote)
    app.route("/add-talk", methods=["POST"])(add_talk)

    # Resister ORM mappings.
    orm.register_mappers()

    # Ensure database is created.
    database.create_schema(app.config["DB_URL"])

    return app
