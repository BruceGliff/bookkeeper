
from typing import Protocol

from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget


class AbstractView(Protocol):
    def set_ctg_list(notused: list[Category]) -> None:
        pass

    def register_ctg_modifier(handler):
        pass

    def register_ctg_adder(handler):
        pass

    def register_ctg_checker(handler):
        pass

    def register_ctg_deleter(handler):
        pass

    def register_bgt_modifier(handler):
        pass
    
    def register_bgt_getter(handler):
        pass


class CategoryPresenter:
    def __init__(self,  view: AbstractView, repository_factory):
        self.view = view
        self.ctg_repo = repository_factory.get(Category)

        self.ctgs = self.ctg_repo.get_all()
        self.view.set_ctg_list(self.ctgs)
        self.view.register_ctg_modifier(self.modify_ctg)
        self.view.register_ctg_adder(self.add_ctg)
        self.view.register_ctg_checker(self.check_name)
        self.view.register_ctg_deleter(self.delete_ctg)

    def modify_ctg(self, ctg: Category) -> None:
        self.ctg_repo.update(ctg)

    def check_name(self, name: str) -> bool:
        if name in [c.name for c in self.ctgs]:
            return False
        return True

    def add_ctg(self, ctg: Category) -> None:
        self.ctg_repo.add(ctg)
        self.ctgs.append(ctg)

    def delete_ctg(self, top_lvl_ctg: Category) -> None:
        queue = [top_lvl_ctg]
        to_delete = list()

        while len(queue) != 0:
            proc = queue.pop()
            to_delete.append(proc)
            queue.extend([x for x in self.ctgs if x.parent == proc.pk])

        for x in to_delete:
            self.ctgs.remove(x)
            self.ctg_repo.delete(x.pk)


class BudgetPresenter:
    def __init__(self,  view: AbstractView, repository_factory):
        self.view = view
        self.repo = repository_factory.get(Budget)
        self.view.register_bgt_modifier(self.modify_bgt)
        self.view.register_bgt_getter(self.get_bgt)

    def modify_bgt(self, bgt: Budget):
        self.repo.update(bgt)

    def get_bgt(self) -> Budget:
        bgts = self.repo.get_all()
        if len(bgts) == 0:
            bgt = Budget(0)
            self.repo.add(bgt)
            bgts.append(bgt)
        
        assert len(bgts) == 1
        return bgts.pop()
    

    

