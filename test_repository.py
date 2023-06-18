import datetime

from sqlalchemy.sql import text

import model
import repository


class TestSqlAlchemyTalkRepository:
    def test_can_add_a_talk(self, session):
        # Add a talk to DB.
        talk = model.Talk(
            ref="talkA",
            title="Test Talk A",
            description="Test Description",
            event_date=datetime.date(2020, 1, 1),
            score=0.5,
        )

        repo = repository.SqlAlchemyTalkRepository(session)
        repo.add(talk)
        session.commit()

        # Check talk is in the DB.
        rows = list(session.execute(text('SELECT ref FROM "talks"')))
        assert rows == [("talkA",)]

    def test_returns_none_if_no_match(self, session):
        repo = repository.SqlAlchemyTalkRepository(session)
        talk = repo.get(ref="talkA")
        assert talk is None

    def test_returns_list_of_talks(self, session):
        # Add a talk to DB.
        talk = model.Talk(
            ref="talkA",
            title="Test Talk A",
            description="Test Description",
            event_date=datetime.date(2020, 1, 1),
            score=0.5,
        )
        repo = repository.SqlAlchemyTalkRepository(session)
        repo.add(talk)
        session.commit()

        # Fetch all talks.
        assert repo.list() == [talk]
