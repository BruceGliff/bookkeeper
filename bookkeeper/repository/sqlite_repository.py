"""
Модуль описывает репозиторий, работающий с sqlite
"""

import sqlite3
from typing import Any
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T


def gettype(attr: Any) -> str:
    # TODO make it more beautiful
    """Returns type in string format for dedicated attr.

    Args:
        attr (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        str: _description_
    """
    if isinstance(attr, int):
        return 'INTEGER'
    return 'TEXT'


class SQLiteRepository(AbstractRepository[T]):
    """_summary_

    Args:
        AbstractRepository (_type_): _description_
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')

        with sqlite3.connect(self.db_file) as con:
            values = [(f'{x}', gettype(getattr(cls, x))) for x in self.fields]
            qstring = ', '.join([f'{x} {ty}' for x, ty in values])
            cur = con.cursor()
            query = (f'CREATE TABLE IF NOT EXISTS {self.table_name} '
                     f'(id INTEGER PRIMARY KEY, {qstring})')
            cur.execute(query)
        con.close()

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        qmarks = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({qmarks})',
                values
            )
            if not cur.lastrowid:
                # TODO cov
                raise ValueError("No assignable pk")
            obj.pk = int(cur.lastrowid)

        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        return []

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """

    def delete(self, pk: int) -> None:
        """ Удалить запись """
