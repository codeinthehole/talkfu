"""
Service/usecase layer.

Responsible for orchestration.
"""
import datetime
from typing import Protocol

import model
import repository


class DatabaseSession(Protocol):
    def commit(self) -> None:
        ...


def add_talk(
    ref: str,
    title: str,
    description: str,
    event_date: datetime.date,
    repository: repository.AbstractTalkRepository,
    session: DatabaseSession,
) -> None:
    # Construct model from request data.
    talk = model.Talk(
        ref=ref,
        title=title,
        description=description,
        event_date=event_date,
        score=0,
    )

    # Add model to DB via repo.
    repository.add(talk)

    # Persist changes.
    session.commit()


class TalkDoesNotExist(Exception):
    pass


def vote_on_talk(
    talk_ref: str,
    username: str,
    num_followers: int,
    repository: repository.AbstractTalkRepository,
    session: DatabaseSession,
) -> None:
    # Look up talk.
    talk = repository.get(talk_ref)
    if not talk:
        raise TalkDoesNotExist(f"Talk {talk_ref} does not exist")

    # Vote.
    user = model.TwitterUser(
        username=username,
        num_followers=num_followers,
    )
    model.vote(talk=talk, user=user)

    # Persist changes.
    session.commit()
