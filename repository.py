import abc

from sqlalchemy.orm import Session

import model


class AbstractTalkRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, talk: model.Talk) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref: str) -> model.Talk | None:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list[model.Talk]:
        raise NotImplementedError


class SqlAlchemyTalkRepository(AbstractTalkRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, talk: model.Talk) -> None:
        self.session.add(talk)

    def get(self, ref: str) -> model.Talk | None:
        return self.session.query(model.Talk).filter_by(ref=ref).first()

    def list(self) -> list[model.Talk]:
        return self.session.query(model.Talk).all()


class FakeTalkRepository(AbstractTalkRepository):
    def __init__(self, talks: list[model.Talk]) -> None:
        self._talks = set(talks)

    def add(self, talk: model.Talk) -> None:
        self._talks.add(talk)

    def get(self, ref: str) -> model.Talk | None:
        matches = [t for t in self._talks if t.ref == ref]
        if len(matches) == 1:
            return matches[0]
        return None

    def list(self) -> list[model.Talk]:
        return list(self._talks)
