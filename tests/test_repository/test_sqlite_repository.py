from bookkeeper.repository.sqlite_repository import SQLiteRepository

import pytest


@pytest.fixture
def custom_class():
    class Custom():
        pk: int = 0
        name: str = "TEST"
        value: int = 42

        def __eq__(self, other) -> bool:
            if not isinstance(other, Custom):
                return NotImplemented
            for x, y in zip(vars(self).items(), vars(other).items()):
                if x != y:
                    return False
            return True

    return Custom


@pytest.fixture
def repo(custom_class):
    return SQLiteRepository("databases/test_database.db", custom_class)


def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    return
    repo.delete(pk)
    assert repo.get(pk) is None