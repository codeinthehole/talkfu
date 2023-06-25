import datetime

from sqlalchemy.sql import text

from talkfu.domain import model


def test_load_and_retrieve(session):
    # Load some rows.
    sql = text(
        "INSERT INTO talks (ref, title, description, event_date, score) VALUES "
        "('talkA', 'Test Talk A', 'Test Description', '2020-01-01', 0.5), "
        "('talkB', 'Test Talk B', 'Test Description', '2020-02-01', 1), "
        "('talkC', 'Test Talk C', 'Test Description', '2020-03-01', 2.4)"
    )
    session.execute(sql)

    talks = session.query(model.Talk).all()

    # Returns the domain model.
    # TODO Check on ordering
    assert talks == [
        model.Talk(
            ref="talkA",
            title="Test Talk A",
            description="Test Description",
            event_date=datetime.date(2020, 1, 1),
            score=0.5,
        ),
        model.Talk(
            ref="talkB",
            title="Test Talk B",
            description="Test Description",
            event_date=datetime.date(2020, 2, 1),
            score=1.0,
        ),
        model.Talk(
            ref="talkC",
            title="Test Talk C",
            description="Test Description",
            event_date=datetime.date(2020, 3, 1),
            score=2.4,
        ),
    ]


def test_insert_load_mutate(session):
    # Insert a talk row.
    initial_talk = model.Talk(
        ref="talkA",
        title="Test Talk A",
        description="Test Description",
        event_date=datetime.date(2020, 1, 1),
        score=0.5,
    )
    session.add(initial_talk)
    session.commit()

    # Fetch talk
    loaded_talk = session.query(model.Talk).filter(model.Talk.ref == "talkA").first()

    # Mutate
    loaded_talk.set_score(1.0)
    session.commit()

    # Re-fetch talk
    reloaded_talk = session.query(model.Talk).filter(model.Talk.ref == "talkA").first()
    assert reloaded_talk.score == 1.0
