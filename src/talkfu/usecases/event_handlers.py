from talkfu.adapters import unit_of_work
from talkfu.domain import events


def send_email(event: events.Event, uow: unit_of_work.AbstractUnitOfWork) -> None:
    breakpoint()
    print(f"Send email: {event}")
