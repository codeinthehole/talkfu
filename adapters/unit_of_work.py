"""
The unit of work abstracts atomic database access.

- It's the place to put all your repositories.
- We don't want the usecase layer to depend on the SQLAlchemy session object, which has a rich
  interface. Better to have a simpler one.
"""
import abc

from . import database, repository


class AbstractUnitOfWork(abc.ABC):
    talks: repository.AbstractTalkRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args: object) -> None:
        # Rollback by default so callers have to explicitly commits.
        self.rollback()

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


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

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
