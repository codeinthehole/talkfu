import datetime

import model


def test_404_for_unknown_talk(client):
    response = client.post(
        "/vote",
        json={"talk_ref": "fake_talk", "username": "fake_user", "num_followers": 1},
    )
    assert response.status_code == 404


def test_201_for_successful_vote(client, session):
    # Add a talk to the DB.
    initial_talk = model.Talk(
        ref="talkA",
        title="Test Talk A",
        description="Test Description",
        event_date=datetime.date(2020, 1, 1),
        score=0.5,
    )
    session.add(initial_talk)
    session.commit()

    response = client.post(
        "/vote",
        json={"talk_ref": "talkA", "username": "fake_user", "num_followers": 10},
    )
    assert response.status_code == 201
