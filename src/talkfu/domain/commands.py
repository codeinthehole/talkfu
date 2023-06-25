import datetime
from dataclasses import dataclass


class Command:
    pass


@dataclass(frozen=True)
class AddTalk(Command):
    ref: str
    title: str
    description: str
    event_date: datetime.date


@dataclass(frozen=True)
class Vote(Command):
    talk_ref: str
    username: str
    num_followers: int
