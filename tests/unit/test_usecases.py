import datetime

import pytest
from adapters import repository, unit_of_work
from domain import model
from usecases import usecases


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self, talks: list[model.Talk]) -> None:
        self.talks = repository.FakeTalkRepository(talks=talks)

    def __enter__(self):
        self.committed = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass


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
            talk_ref=talk.ref, username="fake_user", num_followers=100, uow=uow
        )

        assert talk.score == 2
        assert uow.committed
