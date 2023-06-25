"""
Service/usecase layer.

- Responsible for orchestration of use cases.
- Depends on domain layer internally.
- Depends on unit-of-work for IO operations.
- Arguments to use case fns are Python primitives.
"""
from talkfu.adapters import unit_of_work
from talkfu.domain import commands, model


def add_talk(
    command: commands.AddTalk,
    uow: unit_of_work.AbstractUnitOfWork,
) -> None:
    # Construct model from request data.
    talk = model.Talk(
        ref=command.ref,
        title=command.title,
        description=command.description,
        event_date=command.event_date,
        score=0,
    )
    with uow:
        # Add model to DB via repo.
        uow.talks.add(talk)
        uow.commit()


class TalkDoesNotExist(Exception):
    pass


def vote_on_talk(
    command: commands.Vote,
    uow: unit_of_work.AbstractUnitOfWork,
) -> None:
    with uow:
        # Look up talk.
        talk = uow.talks.get(command.talk_ref)
        if not talk:
            raise TalkDoesNotExist(f"Talk {command.talk_ref} does not exist")

        # Vote.
        user = model.TwitterUser(
            username=command.username,
            num_followers=command.num_followers,
        )
        events = model.vote(talk=talk, user=user)

        # Persist changes.
        uow.commit(events)
