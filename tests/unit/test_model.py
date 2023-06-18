import datetime

from domain import model


def test_talk_score_is_log10_of_voters_twitter_followers():
    talk = model.Talk(
        ref="YT-1",
        title="Test",
        description="Test",
        event_date=datetime.date(2023, 1, 10),
        score=0.0,
    )

    # Vote once
    low_follower_user = model.TwitterUser(username="Jimmy", num_followers=10)
    model.vote(talk, low_follower_user)
    assert talk.score == 1.0

    # Vote again
    high_follower_user = model.TwitterUser(username="Taylor", num_followers=1000)
    model.vote(talk, high_follower_user)
    assert talk.score == 4.0
