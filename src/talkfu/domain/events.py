from dataclasses import dataclass


class Event:
    """
    Value object for a domain event.
    """


@dataclass(frozen=True)
class HighScore(Event):
    pass
