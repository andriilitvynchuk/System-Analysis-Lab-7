import sys

import numpy as np
import pandas as pd
from PyQt5.Qt import QApplication, QFileDialog, QInputDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from cognitive_model import CognitiveModel
from main_window import Ui_MainWindow, _translate


# Entry point
app = QApplication(sys.argv)
app.setApplicationName("Work 8")


def to_float(x):
    try:
        return float(x)
    except ValueError:
        return None


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # setting up ui
        self.setupUi(self)
        self.tableWidget.resizeColumnsToContents()

    def get_A(self):
        A = []
        for i in range(self.tableWidget.rowCount()):
            A_row = []
            for j in range(self.tableWidget.columnCount()):
                val = to_float(self.tableWidget.item(i, j).text())
                if val == None:
                    return None
                A_row.append(val)
            A.append(np.array(A_row))
        return np.array(A)

    @pyqtSlot()
    def buildClicked(self):
        A = self.get_A()
        if A is None:
            QMessageBox.warning(self, "Error", "Error parsing matrix")
            return

        cognitiveModel = CognitiveModel(A)
        cognitiveModel.draw_graph()

    @pyqtSlot()
    def researchClicked(self):
        A = self.get_A()
        if A is None:
            QMessageBox.warning(self, "Error", "Error parsing matrix")

        # researching A
        cognitiveModel = CognitiveModel(A)

        results = "Eigenvalues: "
        results += " ".join(str(x) for x in cognitiveModel.calculate_eigenvalues())
        results += "\n"

        results += "Disturbance stability: "
        results += "True" if cognitiveModel.check_perturbation_stability() else "False"
        results += "\n"

        results += "Value stability: "
        results += "True" if cognitiveModel.check_numerical_stability() else "False"
        results += "\n"
        results += "\n"

        results += "Structural stability: "
        cycles = cognitiveModel.check_structural_stability()
        if not cycles:
            results += "True"
        else:
            cycle_str = lambda x: " - ".join(self.tableWidget.verticalHeaderItem(y).text() for y in x)
            results += "No (" + ", ".join(cycle_str(x) for x in cycles) + ")"
        self.label.setText(results)

    @pyqtSlot()
    def openClicked(self):
        filename = QFileDialog.getOpenFileName(self, "Відкрити файл з данними", ".", "Data file (*.csv)")
        if filename == "":
            return
        self.openLineEdit.setText(filename[0])
        df = pd.read_csv(filename[0])
        self.tableWidget.clear()

        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setColumnCount(len(df))
        self.tableWidget.setRowCount(len(df))

        self.tableWidget.setSortingEnabled(False)

        for i in range(len(df)):
            item = QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("MainWindow", str(i + 1), None))

            item = QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)

        for i in range(len(df)):
            for j in range(len(df)):
                item = QTableWidgetItem()
                item.setText(_translate("MainWindow", str(df.iloc[i, j]), None))
                self.tableWidget.setItem(i, j, item)

        self.tableWidget.resizeColumnsToContents()

    @pyqtSlot()
    def addClicked(self):

        name = str(self.tableWidget.rowCount() + 1)
        r = self.tableWidget.rowCount()
        self.tableWidget.setColumnCount(r + 1)
        self.tableWidget.setRowCount(r + 1)
        self.tableWidget.setHorizontalHeaderItem(r, QTableWidgetItem(name))
        self.tableWidget.setVerticalHeaderItem(r, QTableWidgetItem(name))

        for i in range(r + 1):
            item = "0"
            self.tableWidget.setItem(i, r, QTableWidgetItem(item))
            self.tableWidget.setItem(r, i, QTableWidgetItem(item))

        self.tableWidget.resizeColumnsToContents()

    @pyqtSlot()
    def removeClicked(self):
        selected_items = self.tableWidget.selectedItems()

        k = selected_items[0]
        r = k.row()
        c = k.column()
        self.tableWidget.removeColumn(c)
        self.tableWidget.removeRow(c)
        if r != c:
            self.tableWidget.removeColumn(r)
            self.tableWidget.removeRow(r)

        self.tableWidget.resizeColumnsToContents()


mainWindow = MainWindow()
mainWindow.setWindowTitle("Lab#8 Yaroslavskyi Doroshchuk Barabash Nogol")
mainWindow.show()
sys.exit(app.exec_())
