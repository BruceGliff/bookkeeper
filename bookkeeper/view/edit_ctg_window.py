"""
Widget of editing categories
"""

from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem)


def set_data(table: QTreeWidget, data: list[str]) -> None:
    stf = QTreeWidgetItem(table, ['1 Продукты'])
    book = QTreeWidgetItem(table, ['1 Книги'])
    meet = QTreeWidgetItem(stf, ['2 Мясо'])
    fish = QTreeWidgetItem(stf, ['2 Рыба'])


class EditCtgWindow(QWidget):
    def __init__(self, ctgs: list[str]) -> None:
        super().__init__()

        self.setWindowTitle("Изменение категорий")

        layout = QtWidgets.QVBoxLayout()

        ctgs_widget = QtWidgets.QTreeWidget()
        ctgs_widget.setColumnCount(1)
        ctgs_widget.setHeaderLabel('Категории')
        set_data(ctgs_widget, ctgs)

        layout.addWidget(ctgs_widget)
        self.setLayout(layout)
