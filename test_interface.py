def test_404_for_unknown_talk(client):
    response = client.post(
        "/vote",
        json={"talk_ref": "fake_talk", "username": "fake_user", "num_followers": 1},
    )
    assert response.status_code == 404


def test_a_talk_can_be_added(client):
    response = client.post(
        "/add-talk",
        json={
            "ref": "bible1",
            "title": "The Bible",
            "description": "XXX",
            "event_date": "2020-01-01",
        },
    )
    assert response.status_code == 201


def test_201_for_successful_vote(client):
    # Create a talk
    response = client.post(
        "/add-talk",
        json={
            "ref": "bible1",
            "title": "The Bible",
            "description": "XXX",
            "event_date": "2020-01-01",
        },
    )
    assert response.status_code == 201

    # Vote on it.
    response = client.post(
        "/vote",
        json={"talk_ref": "bible1", "username": "fake_user", "num_followers": 10},
    )
    assert response.status_code == 201
