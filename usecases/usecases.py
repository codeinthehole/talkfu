"""
Service/usecase layer.

- Responsible for orchestration.
- Depends on domain layer internally
- Arguments to use case fns are Python primitives
- Depends on abstractions for repository and database session.
"""
import datetime
from typing import Protocol

from adapters import repository
from domain import model


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
