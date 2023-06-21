"""
The unit of work abstracts atomic database access.

- It's the place to put all your repositories.
- We don't want the usecase layer to depend on the SQLAlchemy session object, which has a rich
  interface. Better to have a simpler one.
"""
import abc

from talkfu.domain import model
from talkfu.usecases import message_bus

from . import database, repository


class AbstractUnitOfWork(abc.ABC):
    talks: repository.AbstractTalkRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args: object) -> None:
        # Rollback by default so callers have to explicitly commits.
        self.rollback()

    @abc.abstractmethod
    def commit(self, events: list[model.Event] | None = None) -> None:
        if events is not None:
            self._publish_events(events)

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    def _publish_events(self, events: list[model.Event]) -> None:
        for event in events:
            message_bus.handle(event)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, db_url: str) -> None:
        self._session_factory = database.get_session_factory(db_url)

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self._session = self._session_factory()
        self.talks = repository.SqlAlchemyTalkRepository(self._session)
        return self

    def __exit__(self, *args: object) -> None:
        super().__exit__(*args)
        self._session.close()

    def commit(self, events: list[model.Event] | None = None) -> None:
        # The state should be committed BEFORE we trigger any event handlers.
        self._session.commit()
        super().commit(events=events)

    def rollback(self) -> None:
        self._session.rollback()
