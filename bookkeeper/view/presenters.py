
from typing import Protocol

from bookkeeper.models.category import Category


class AbstractView(Protocol):
    def set_ctg_list(notused: list[Category]) -> None:
        pass

    def register_ctg_modifier(handler):
        pass


class CategoryPresenter:
    def __init__(self,  view: AbstractView, repository_factory):
        self.view = view
        self.ctg_repo = repository_factory.get(Category)

        self.ctgs = self.ctg_repo.get_all()
        self.view.set_ctg_list(self.ctgs)
        self.view.register_ctg_modifier(self.modify_ctg)

    def modify_ctg(self, ctg: Category) -> None:
        self.ctg_repo.update(ctg)
        #self.view.set_ctg_list(self.ctgs)

    def add_ctg(self, name, parent):
        if name in [c.name for c in self.ctgs]:
            raise ValueError(f'Category {name} already present.')
        
        ctg = Category(name, parent)
        self.ctg_repo.add(ctg)
        self.ctgs.append(ctg)
        self.view.set_ctg_list(self.ctgs)
