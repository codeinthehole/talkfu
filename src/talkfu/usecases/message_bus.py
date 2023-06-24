from typing import Any, Callable, TypeAlias

from talkfu.adapters import unit_of_work
from talkfu.domain import commands, events
from talkfu.usecases import usecases

from . import event_handlers

Message: TypeAlias = commands.Command | events.Event


def handle(
    message: Message,
    uow: unit_of_work.AbstractUnitOfWork,
) -> None:
    # Command/event handlers can add more messages to the queue.
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, commands.Command):
            _handle_command(message, queue, uow)
        elif isinstance(message, events.Event):
            _handle_event(message, queue, uow)
        else:
            raise ValueError(f"Unknown message type {message}")


def _handle_command(
    command: commands.Command,
    queue: list[Message],
    uow: unit_of_work.AbstractUnitOfWork,
) -> None:
    for handler in _get_command_handlers(command):
        handler(command, uow)
        queue.extend(uow.collect_events())


def _handle_event(
    event: events.Event,
    queue: list[Message],
    uow: unit_of_work.AbstractUnitOfWork,
) -> None:
    for handler in _get_event_handlers(event):
        handler(event, uow)
        queue.extend(uow.collect_events())


def _get_command_handlers(
    command: commands.Command,
) -> list[Callable[[Any, unit_of_work.AbstractUnitOfWork], None]]:
    handlers: dict[
        type[commands.Command],
        list[Callable[[Any, unit_of_work.AbstractUnitOfWork], None]],
    ] = {
        commands.AddTalk: [usecases.add_talk],
        commands.Vote: [usecases.vote_on_talk],
    }
    return handlers.get(type(command), [])


def _get_event_handlers(
    event: events.Event,
) -> list[Callable[[Any, unit_of_work.AbstractUnitOfWork], None]]:
    handlers: dict[
        type[events.Event], list[Callable[[Any, unit_of_work.AbstractUnitOfWork], None]]
    ] = {
        events.HighScore: [event_handlers.send_email],
    }
    return handlers.get(type(event), [])
