"""
Widget of expence table
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QWidget, QTableWidget, QMenu, QMessageBox, QTableWidgetItem)
from datetime import datetime

from .presenters import ExpensePresenter
from bookkeeper.repository.repository_factory import RepositoryFactory
from bookkeeper.models.expense import Expense


class TableRow():
    def __init__(self, exp: Expense):
        self.exp = exp


class TableItem(QTableWidgetItem):
    def __init__(self, row: TableRow):
        super().__init__()
        self.row = row
        self.restore()
    
    def validate(self) -> bool:
        return True

    def restore(self):
        self.setText(self.row.exp.comment)

    def update(self):
        self.row.exp.comment = self.text()


class TableAmountItem(TableItem):
    def __init__(self, row: TableRow):
        super().__init__(row)

    def validate(self) -> bool:
        try:
            float(self.text())
        except ValueError:
            return False
        return True

    def restore(self):
        self.setText(str(self.row.exp.amount))

    def update(self):
        self.row.exp.amount = float(self.text())


class TableCategoryItem(TableItem):
    def __init__(self, row: TableRow):
        super().__init__(row)

    def validate(self) -> bool:
        # TODO
        return True
    
    def restore(self):
        self.setText(str(self.row.exp.category))
    
    def update(self):
        self.row.exp.category = int(self.text())


class TableDateItem(TableItem):
    def __init__(self, row: TableRow):
        super().__init__(row)
        self.setFlags(self.flags() & ~QtCore.Qt.ItemIsEditable)

    def restore(self):
        self.setText(str(self.row.exp.expense_date))


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

        self.itemChanged.connect(self.update_exp_event)

    def update_exp_event(self, exp_item: TableItem):
        if not exp_item.validate():
            self.itemChanged.disconnect()
            QMessageBox.critical(self, 'Ошибка', f'Нужно ввести число')
            exp_item.restore()
            self.itemChanged.connect(self.update_exp_event)
            return

        exp_item.update()
        self.parent.exp_modifier(exp_item.row.exp)

    def add_expense(self, exp: Expense) -> TableAmountItem:
        self.itemChanged.disconnect()
        rc = self.rowCount()
        self.setRowCount(rc+1)
        row = TableRow(exp)
        self.setItem(rc, 0, TableDateItem(row))
        self.setItem(rc, 1, TableAmountItem(row))
        self.setItem(rc, 2, TableCategoryItem(row))
        self.setItem(rc, 3, TableItem(row))
        self.itemChanged.connect(self.update_exp_event)
        return self.item(rc, 1)

    def delete_exp_event(self):
        row = self.currentRow()
        if row == -1:
            return
        confirm = QMessageBox.warning(self, 'Внимание',
                                      'Вы уверены, что хотите удалить текущую запись?"',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if confirm == QMessageBox.No:
            return
        self.removeRow(row)
        self.parent.exp_deleter(row)

    def add_exp_event(self):
        exp = Expense(category=5) #TODO getCategory
        self.add_expense(exp)
        self.parent.exp_adder(exp)

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

        #self.table.itemChanged.connect(self.table.update_exp_event)

        #exp = Expense(amount=100.0, category=5, comment="ASD")
        #self.exp_adder(exp)
        #print(f'ADDED {exp}')

    def register_exp_adder(self, handler):
        self.exp_adder = handler

    def register_exp_deleter(self, handler):
        self.exp_deleter = handler
    
    def register_exp_modifier(self, handler):
        self.exp_modifier = handler

    def set_exp_list(self, data: list[Expense]):
        for x in data:
            self.table.add_expense(x)
        
