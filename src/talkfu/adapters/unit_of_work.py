"""
The unit of work abstracts atomic database access.

- It's the place to put all your repositories.
- We don't want the usecase layer to depend on the SQLAlchemy session object, which has a rich
  interface. Better to have a simpler one.
"""
import abc

from talkfu.domain import events

from . import database, repository


class AbstractUnitOfWork(abc.ABC):
    talks: repository.AbstractTalkRepository
    domain_events: list[events.Event]

    def __enter__(self) -> "AbstractUnitOfWork":
        # Reset events when we start a new transaction.
        self.domain_events = []
        return self

    def __exit__(self, *args: object) -> None:
        # Rollback by default so callers have to explicitly commit.
        self.rollback()

    def commit(self, events: list[events.Event] | None = None) -> None:
        if events:
            self.domain_events = events

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    def collect_events(self) -> list[events.Event]:
        """
        Return and reset the collected events.
        """
        events = self.domain_events
        self.domain_events = []
        return events


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, db_url: str) -> None:
        self._session_factory = database.get_session_factory(db_url)

    def __enter__(self) -> AbstractUnitOfWork:
        self._session = self._session_factory()
        self.talks = repository.SqlAlchemyTalkRepository(self._session)
        return super().__enter__()

    def __exit__(self, *args: object) -> None:
        super().__exit__(*args)
        self._session.close()

    def commit(self, events: list[events.Event] | None = None) -> None:
        super().commit(events)
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
