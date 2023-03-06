"""
Widget of budget table
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QMessageBox)
from bookkeeper.models.budget import Budget


def get_expenses_from_expenses_tbl():
    return [1, 2, 3]


def get_budget():
    return Budget(100)


class LimitDayItem(QTableWidgetItem):
    def __init__(self, bgt: Budget):
        super().__init__()
        self.update(bgt)

    def get_value(self):
        try:
            return float(self.text())
        except ValueError:
            return None

    def update(self, bgt: Budget):
        #TODO change string if budget changes
        self.bgt = bgt
        self.setText(str(self.bgt.amount))
        pass


class LimitWeekItem(QTableWidgetItem):
    def __init__(self, bgt: Budget):
        super().__init__()
        self.update(bgt)

    def get_value(self):
        try:
            return float(self.text()) / 7
        except ValueError:
            return None

    def update(self, bgt: Budget):
        #TODO change string if budget changes
        self.bgt = bgt
        self.setText(str(self.bgt.amount * 7))
        pass


class LimitMonthItem(QTableWidgetItem):
    def __init__(self, bgt: Budget):
        super().__init__()
        self.update(bgt)

    def get_value(self):
        try:
            return float(self.text()) / 30
        except ValueError:
            return None

    def update(self, bgt: Budget):
        #TODO change string if budget changes
        self.bgt = bgt
        self.setText(str(self.bgt.amount * 30))
        pass


class BudgetWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Бюджет")
        layout.addWidget(message)

        self.expenses_table = QtWidgets.QTableWidget(2, 3)
        self.expenses_table.setColumnCount(2)
        self.expenses_table.setRowCount(3)
        self.expenses_table.setHorizontalHeaderLabels("Сумма "
                                                      "Бюджет ".split())
        self.expenses_table.setVerticalHeaderLabels("День "
                                                    "Неделя "
                                                    "Месяц ".split())

        header = self.expenses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        for i in range(3):
            lost_item = QtWidgets.QTableWidgetItem()
            lost_item.setFlags(lost_item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.expenses_table.setItem(i, 0, lost_item)
        
        bgt: Budget = Budget(1)
        self.expenses_table.setItem(0, 1, LimitDayItem(bgt))
        self.expenses_table.setItem(1, 1, LimitWeekItem(bgt))
        self.expenses_table.setItem(2, 1, LimitMonthItem(bgt))
        self.expenses_table.itemChanged.connect(self.edit_bgt_event)

        layout.addWidget(self.expenses_table)
        self.setLayout(layout)

        expenses = get_expenses_from_expenses_tbl()
        bgt = get_budget()

        self.update_expenses(expenses)
        self.update_budget(bgt)


    def edit_bgt_event(self, bgt_item: QTableWidgetItem):
        value = bgt_item.get_value()
        if value is None:
            QMessageBox.critical(self, 'Ошибка', 'Используйте только числа.')
        else:
            bgt_item.bgt.amount = value
            #TODO update repo

        self.update_budget(bgt_item.bgt)

    def update_expenses(self, exs: list[float]) -> None:
        pass

    def update_budget(self, bgt: Budget) -> None:
        self.expenses_table.itemChanged.disconnect()
        for i in range(3):
            self.expenses_table.item(i, 1).update(bgt)
        self.expenses_table.itemChanged.connect(self.edit_bgt_event)
