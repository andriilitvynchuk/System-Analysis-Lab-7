from typing import Any, NoReturn

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QWidget,
)


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(string: str) -> str:
        return string


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context: Any, text: str, disambig: Any) -> str:
        return QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context: Any, text: str, disambig: Any) -> str:
        return QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: Any, col_count: int, row_count: int, default_adj_matrix: np.ndarray) -> NoReturn:
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1024, 600)

        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.tableWidget = QTableWidget(self.centralWidget)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))

        self.tableWidget.setColumnCount(col_count)
        self.tableWidget.setRowCount(row_count)

        for index in range(row_count):
            item = QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(index, item)

        for index in range(col_count):
            item = QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(index, item)

        for index_i in range(row_count):
            for index_j in range(col_count):
                item = QTableWidgetItem()
                self.tableWidget.setItem(index_i, index_j, item)

        self.openLineEdit = QLineEdit(self.centralWidget)
        self.openLineEdit.setMinimumSize(QtCore.QSize(90, 20))
        self.openLineEdit.setObjectName(_fromUtf8("openLineEdit"))
        self.gridLayout.addWidget(self.openLineEdit, 0, 1, 1, 3)

        self.openButton = QPushButton(self.centralWidget)
        self.openButton.setMinimumSize(QtCore.QSize(30, 30))
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.gridLayout.addWidget(self.openButton, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.tableWidget, 2, 1, 4, 1)
        self.buildButton = QPushButton(self.centralWidget)
        self.buildButton.setMinimumSize(QtCore.QSize(90, 50))
        self.buildButton.setObjectName(_fromUtf8("buildButton"))
        self.gridLayout.addWidget(self.buildButton, 2, 0, 1, 1)
        self.label = QTextBrowser(self.centralWidget)
        self.label.setAutoFillBackground(True)
        self.label.setMinimumSize(QtCore.QSize(0, 250))
        self.label.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 6, 1, 1, 1)
        self.researchButton = QPushButton(self.centralWidget)
        self.researchButton.setMinimumSize(QtCore.QSize(90, 50))
        self.researchButton.setObjectName(_fromUtf8("researchButton"))
        self.gridLayout.addWidget(self.researchButton, 6, 0, 1, 1)
        self.addButton = QPushButton(self.centralWidget)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.gridLayout.addWidget(self.addButton, 3, 0, 1, 1)
        self.removeButton = QPushButton(self.centralWidget)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.gridLayout.addWidget(self.removeButton, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow, col_count, row_count, default_adj_matrix)
        self.buildButton.clicked.connect(MainWindow.buildClicked)
        self.researchButton.clicked.connect(MainWindow.researchClicked)
        self.addButton.clicked.connect(MainWindow.addClicked)
        self.removeButton.clicked.connect(MainWindow.removeClicked)
        self.openButton.clicked.connect(MainWindow.openClicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(
        self, MainWindow: Any, col_count: int, row_count: int, default_adj_matrix: np.ndarray
    ) -> NoReturn:
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

        for index in range(row_count):
            item = self.tableWidget.verticalHeaderItem(index)
            item.setText(_translate("MainWindow", f"{index + 1}", None))

        for index in range(col_count):
            item = self.tableWidget.horizontalHeaderItem(index)
            item.setText(_translate("MainWindow", f"{index + 1}", None))

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        for index_i in range(row_count):
            for index_j in range(col_count):
                item = self.tableWidget.item(index_i, index_j)
                item.setText(_translate("MainWindow", str(default_adj_matrix[index_i, index_j]), None))

        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.openButton.setText(_translate("MainWindow", "Відкрити файл", None))
        self.buildButton.setText(_translate("MainWindow", "Намалювати граф", None))
        self.label.setText(_translate("MainWindow", "", None))
        self.openLineEdit.setText(_translate("MainWindow", "data/ukraine.txt", None))
        self.researchButton.setText(_translate("MainWindow", "Виконати", None))
        self.addButton.setText(_translate("MainWindow", "Додати фактор", None))
        self.removeButton.setText(_translate("MainWindow", "Видалити фактор", None))
