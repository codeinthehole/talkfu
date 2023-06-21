from typing import Callable

from talkfu.domain import model


def handle(event: model.Event) -> None:
    for handler in HANDLERS.get(type(event), []):
        handler(event)


def send_email(event: model.Event) -> None:
    print(f"Send email: {event}")


HANDLERS: dict[type[model.Event], list[Callable[[model.Event], None]]] = {
    model.HighScore: [send_email],
}
