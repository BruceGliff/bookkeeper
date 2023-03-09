
from .abstract_repository import AbstractRepository
from .sqlite_repository import SQLiteRepository
from abc import ABC, abstractmethod


class AbsRepoFactory(ABC):
    @abstractmethod
    def get(self, cls: type) -> AbstractRepository:
        """__summary
        """


class RepositoryFactory(AbsRepoFactory):
    def get(self, cls: type) -> AbstractRepository:
        return SQLiteRepository[cls]("databases/ui_client.db", cls)
