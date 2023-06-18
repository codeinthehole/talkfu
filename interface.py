from typing import Any

import flask

import database
import model
import orm


def vote() -> tuple[str, int]:
    # DB connection
    session = database.get_session(flask.current_app.config["DB_URL"])

    # Get talk directly from SQLAlchemy.
    talk_ref = flask.request.json["talk_ref"]
    talk = session.query(model.Talk).filter_by(ref=talk_ref).first()
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

    # Resister ORM mappings.
    orm.register_mappers()

    # Ensure database is created.
    database.create_schema(app.config["DB_URL"])

    return app
