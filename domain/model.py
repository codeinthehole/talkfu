import datetime
import math
from dataclasses import dataclass

# A mix of value objects, entities and service functions.


@dataclass
class TwitterUser:
    # Value object as it won't mutate in this use case.
    def __init__(self, username: str, num_followers: int):
        self.username = username
        self.num_followers = num_followers


class Talk:
    # An entity

    def __init__(
        self,
        ref: str,
        title: str,
        description: str,
        event_date: datetime.date,
        score: float,
    ):
        self.ref = ref
        self.title = title
        self.description = description
        self.event_date = event_date
        self.score = score

    def __repr__(self) -> str:
        return f"<Talk {self.ref}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.ref == self.ref

    def __hash__(self) -> int:
        return hash(self.ref)

    def set_score(self, new_score: float) -> None:
        self.score = new_score


def vote(talk: Talk, user: TwitterUser) -> None:
    new_score = talk.score + math.log10(user.num_followers)
    talk.set_score(new_score)
