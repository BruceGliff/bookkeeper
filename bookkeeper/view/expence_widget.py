"""
Widget of expence table
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QWidget, QTableWidget, QMenu, QMessageBox)

from .presenters import ExpensePresenter
from bookkeeper.repository.repository_factory import RepositoryFactory
from bookkeeper.models.expense import Expense


def set_data(table: QTableWidget, data: list[list[str]]) -> None:
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            table.setItem(i, j, QtWidgets.QTableWidgetItem(x.capitalize()))


class Table(QTableWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setColumnCount(4)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels("Дата "
                                       "Сумма "
                                       "Категория "
                                       "Комментарий".split())

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.verticalHeader().hide()

        self.menu = QMenu(self)
        self.menu.addAction('Добавить').triggered.connect(self.add_exp_event)
        self.menu.addAction('Удалить').triggered.connect(self.delete_exp_event)

    def add_expense(self, exp: Expense) -> None:
        rc = self.rowCount()
        print(exp)
        self.setRowCount(rc+1)
        ex_item = QtWidgets.QTableWidgetItem(str(exp.expense_date))
        ex_item.setFlags(ex_item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(rc, 0, ex_item)
        self.setItem(rc, 1, QtWidgets.QTableWidgetItem(str(exp.amount)))
        self.setItem(rc, 2, QtWidgets.QTableWidgetItem(str(exp.category)))
        self.setItem(rc, 3, QtWidgets.QTableWidgetItem(exp.comment))

    def delete_exp_event(self):
        row = self.currentRow()
        confirm = QMessageBox.warning(self, 'Внимание',
                                      'Вы уверены, что хотите удалить текущую запись?"',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.No:
            return
        self.removeRow(row)
        self.parent.exp_deleter(row)

    def add_exp_event(self):
        exp = Expense(comment="IKLETHLSEDFHKL")
        self.add_expense(exp)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())


class ExpenceWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Последние расходы")
        layout.addWidget(message)

        self.table = Table(self)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.presenter = ExpensePresenter(self, RepositoryFactory())

        #exp = Expense(amount=100.0, category=5, comment="ASD")
        #self.exp_adder(exp)
        #print(f'ADDED {exp}')

    def register_exp_adder(self, handler):
        self.exp_adder = handler

    def register_exp_deleter(self, handler):
        self.exp_deleter = handler

    def set_exp_list(self, data: list[Expense]):
        for x in data:
            self.table.add_expense(x)
        
