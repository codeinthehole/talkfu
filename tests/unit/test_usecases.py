import datetime

import pytest
from adapters import repository
from domain import model
from usecases import usecases


class FakeSession:
    committed = False

    def commit(self) -> None:
        self.committed = True


class TestAddTalk:
    def test_adds_talk_to_repo(self):
        repo = repository.FakeTalkRepository(talks=[])
        session = FakeSession()

        usecases.add_talk(
            ref="bible1",
            title="The Bible",
            description="XXX",
            event_date=datetime.date(2020, 1, 1),
            repository=repo,
            session=session,
        )

        assert len(repo.list()) == 1
        assert session.committed


class TestVoteOnTalk:
    def test_raises_exception_if_talk_not_found(self):
        repo = repository.FakeTalkRepository(talks=[])
        session = FakeSession()

        with pytest.raises(usecases.TalkDoesNotExist):
            usecases.vote_on_talk(
                talk_ref="bible1",
                username="fake_user",
                num_followers=123,
                repository=repo,
                session=session,
            )

    def test_saves_new_score(self):
        talk = model.Talk(
            ref="bible1",
            title="The Bible",
            description="XXX",
            event_date=datetime.date(2020, 1, 1),
            score=0,
        )
        repo = repository.FakeTalkRepository(talks=[talk])
        session = FakeSession()

        usecases.vote_on_talk(
            talk_ref=talk.ref,
            username="fake_user",
            num_followers=100,
            repository=repo,
            session=session,
        )

        assert talk.score == 2
        assert session.committed
