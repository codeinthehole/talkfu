"""
Service/usecase layer.

- Responsible for orchestration of use cases.
- Depends on domain layer internally.
- Depends on unit-of-work for IO operations.
- Arguments to use case fns are Python primitives.
"""
import datetime

from adapters import unit_of_work
from domain import model


def add_talk(
    ref: str,
    title: str,
    description: str,
    event_date: datetime.date,
    uow: unit_of_work.AbstractUnitOfWork,
) -> None:
    # Construct model from request data.
    talk = model.Talk(
        ref=ref,
        title=title,
        description=description,
        event_date=event_date,
        score=0,
    )
    with uow:
        # Add model to DB via repo.
        uow.talks.add(talk)
        uow.commit()


class TalkDoesNotExist(Exception):
    pass


def vote_on_talk(
    talk_ref: str,
    username: str,
    num_followers: int,
    uow: unit_of_work.AbstractUnitOfWork,
) -> None:
    with uow:
        # Look up talk.
        talk = uow.talks.get(talk_ref)
        if not talk:
            raise TalkDoesNotExist(f"Talk {talk_ref} does not exist")

        # Vote.
        user = model.TwitterUser(
            username=username,
            num_followers=num_followers,
        )
        model.vote(talk=talk, user=user)

        # Persist changes.
        uow.commit()
