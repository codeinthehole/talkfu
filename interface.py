import datetime
from typing import Any

import flask

import database
import model
import orm
import repository


def add_talk() -> tuple[str, int]:
    # Set-up repository.
    session = database.get_session(flask.current_app.config["DB_URL"])
    repo = repository.SqlAlchemyTalkRepository(session)

    # Construct model from request data.
    talk = model.Talk(
        ref=flask.request.json["ref"],
        title=flask.request.json["title"],
        description=flask.request.json["description"],
        event_date=datetime.datetime.strptime(
            flask.request.json["event_date"], "%Y-%m-%d"
        ).date(),
        score=0,
    )

    # Add model to DB via repo.
    repo.add(talk)

    # Persist changes.
    session.commit()

    return "", 201


def vote() -> tuple[str, int]:
    # Set-up repository.
    session = database.get_session(flask.current_app.config["DB_URL"])
    repo = repository.SqlAlchemyTalkRepository(session)

    # Get talk directly from SQLAlchemy.
    talk_ref = flask.request.json["talk_ref"]
    talk = repo.get(talk_ref)
    if not talk:
        flask.abort(404)

    # Vote.
    user = model.TwitterUser(
        username=flask.request.json["username"],
        num_followers=flask.request.json["num_followers"],
    )
    model.vote(talk=talk, user=user)

    # Persist changes.
    session.commit()

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
