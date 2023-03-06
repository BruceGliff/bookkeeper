"""
Widget of editing categories
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QWidget, QTreeWidgetItem, QMenu)

from .presenters import CategoryPresenter
from bookkeeper.repository.repository_factory import RepositoryFactory
from bookkeeper.models.category import Category


"""
def set_data(table: QTreeWidget, data: list[str]) -> None:
    stf = QTreeWidgetItem(table, ['1 Продукты'])
    book = QTreeWidgetItem(table, ['1 Книги'])
    meet = QTreeWidgetItem(stf, ['2 Мясо'])
    fish = QTreeWidgetItem(stf, ['2 Рыба'])
"""

def handler_error(widget, handler):
    def inner(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except ValueError as ex:
            QMessageBox.critical(self, 'Ошибка', str(ex))
    return inner


class CategoryItem(QTreeWidgetItem):
    def __init__(self, parent, ctg: Category):
        super().__init__(parent, [ctg.name])
        self.ctg = ctg
    
    def update(self, name: str):
        self.ctg.name = name
    
    # TODO this does not work if ctg.name is changed.
    def __str__(self):
        return self.ctg.name


class EditCtgWindow(QWidget):

    def __init__(self, ctgs: list[str]):
        super().__init__()

        self.setWindowTitle("Изменение категорий")

        layout = QtWidgets.QVBoxLayout()

        self.ctgs_widget = QtWidgets.QTreeWidget()
        self.ctgs_widget.setColumnCount(1)
        self.ctgs_widget.setHeaderLabel('Категории')

        layout.addWidget(self.ctgs_widget)
        self.setLayout(layout)
        self.presenter = CategoryPresenter(self, RepositoryFactory())

        self.menu = QMenu(self)
        self.menu.addAction('Добавить').triggered.connect(self.add_ctg_event)
        self.menu.addAction('Удалить').triggered.connect(self.delete_ctg_event)

        self.ctgs_widget.itemChanged.connect(self.edit_ctg_event)

    #def register_ctg_adder(self, handler):
    #    self.ctg_adder = handler_error(self, handler)

    def register_ctg_modifier(self, handler):
        self.ctg_modifier = handler_error(self, handler)

    def add_ctg(self):
        name = "c"
        parent = 0
        self.ctg_adder(name, parent)

    def set_ctg_list(self, ctgs: list[Category]) -> None:
        table = self.ctgs_widget
        uniq_pk: dict[int, CategoryItem] = {}

        for x in ctgs:
            pk = x.pk
            parent = x.parent

            # default parent is table.
            parent_ctg = table
            if parent is not None:
                parent_ctg = uniq_pk.get(int(parent))

            ctg_item = CategoryItem(parent_ctg, x)
            ctg_item.setFlags(ctg_item.flags() | QtCore.Qt.ItemIsEditable)
            uniq_pk.update({pk: ctg_item})

    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())

    def edit_ctg_event(self, ctg_item: CategoryItem, column: int):
        ctg_item.update(ctg_item.text(column))
        self.ctg_modifier(ctg_item.ctg)

    def add_ctg_event(self):
        ctg = self.ctgs_widget.currentItem()
        print(f'Adding {ctg}')

    def delete_ctg_event(self):
        ctg = self.ctgs_widget.currentItem()
        print(f'Deleting {ctg}')


