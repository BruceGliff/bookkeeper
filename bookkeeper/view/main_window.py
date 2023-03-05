"""
MainWindow view
"""

from PySide6 import QtWidgets
from PySide6.QtWidgets import (QWidget)

from .expence_widget import ExpenceWidget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bookkeeper")

        layout = QtWidgets.QVBoxLayout()
        expence = ExpenceWidget()
        budget = QtWidgets.QLabel("PLACEHOLDER FOR BUDGET")
        edit_field = QtWidgets.QLabel("PLACEHOLDER FOR EDITING")

        layout.addWidget(expence)
        layout.addWidget(budget)
        layout.addWidget(edit_field)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
