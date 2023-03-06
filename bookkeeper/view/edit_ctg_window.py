"""
Widget of editing categories
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QWidget, QTreeWidgetItem, QMenu, QMessageBox)

from .presenters import CategoryPresenter
from bookkeeper.repository.repository_factory import RepositoryFactory
from bookkeeper.models.category import Category


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
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
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

    def register_ctg_adder(self, handler):
        self.ctg_adder = handler_error(self, handler)

    def register_ctg_modifier(self, handler):
        self.ctg_modifier = handler_error(self, handler)

    def register_ctg_checker(self, handler):
        self.ctg_checker = handler_error(self, handler)

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
            uniq_pk.update({pk: ctg_item})

    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())

    def edit_ctg_event(self, ctg_item: CategoryItem, column: int):
        if not self.ctg_checker(ctg_item.ctg):
            ctg_item.setText(ctg_item.ctg.name)
            pass

        if ctg_item.ctg.pk != 0:
            ctg_item.update(ctg_item.text(column))
            self.ctg_modifier(ctg_item.ctg)
        else:
            ctg_item.update(ctg_item.text(column))
            self.ctg_adder(ctg_item.ctg)

    def add_ctg_event(self):
        ctg_items = self.ctgs_widget.selectedItems()
        if len(ctg_items) == 0:
            parent_item = self.ctgs_widget
            parent_pk = None
        else:
            assert len(ctg_items) == 1
            parent_item = ctg_items.pop()
            parent_pk = parent_item.ctg.pk

        self.ctgs_widget.itemChanged.disconnect()
        new_ctg = CategoryItem(parent_item, Category(parent=parent_pk))
        self.ctgs_widget.itemChanged.connect(self.edit_ctg_event)
        self.ctgs_widget.setCurrentItem(new_ctg)
        self.ctgs_widget.edit(self.ctgs_widget.currentIndex())

    def delete_ctg_event(self):
        ctg = self.ctgs_widget.currentItem()
        print(f'Deleting {ctg}')

    def dummy(self): pass


