import datetime

import pytest

from talkfu.adapters import repository, unit_of_work
from talkfu.domain import model
from talkfu.usecases import usecases


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self, talks: list[model.Talk]) -> None:
        self.talks = repository.FakeTalkRepository(talks=talks)
        self.events: list[model.Event] = []

    def __enter__(self):
        self.committed = False

    def commit(self, events: list[model.Event] | None = None) -> None:
        self.committed = True
        super().commit(events)

    def rollback(self) -> None:
        pass

    def _publish_events(self, events: list[model.Event]) -> None:
        self.events = events


class TestAddTalk:
    def test_adds_talk_to_repo(self):
        uow = FakeUnitOfWork(talks=[])

        usecases.add_talk(
            ref="bible1",
            title="The Bible",
            description="XXX",
            event_date=datetime.date(2020, 1, 1),
            uow=uow,
        )

        assert len(uow.talks.list()) == 1
        assert uow.committed


class TestVoteOnTalk:
    def test_raises_exception_if_talk_not_found(self):
        uow = FakeUnitOfWork(talks=[])

        with pytest.raises(usecases.TalkDoesNotExist):
            usecases.vote_on_talk(
                talk_ref="bible1",
                username="fake_user",
                num_followers=123,
                uow=uow,
            )

    def test_saves_new_score(self):
        talk = model.Talk(
            ref="bible1",
            title="The Bible",
            description="XXX",
            event_date=datetime.date(2020, 1, 1),
            score=0,
        )
        uow = FakeUnitOfWork(talks=[talk])

        usecases.vote_on_talk(
            talk_ref=talk.ref, username="fake_user", num_followers=100000, uow=uow
        )

        assert talk.score == 5.0
        assert uow.committed

    def test_publishes_event_on_high_follower_count_vote(self):
        talk = model.Talk(
            ref="bible1",
            title="The Bible",
            description="XXX",
            event_date=datetime.date(2020, 1, 1),
            score=0,
        )
        uow = FakeUnitOfWork(talks=[talk])

        usecases.vote_on_talk(
            talk_ref=talk.ref, username="fake_user", num_followers=100000, uow=uow
        )

        assert talk.score == 5.0
        assert uow.committed

        # Check events were passed to UoW.
        assert len(uow.events) == 1
        assert isinstance(uow.events[0], model.HighScore)
