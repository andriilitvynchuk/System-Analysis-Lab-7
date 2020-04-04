import sys
from typing import Any, List, NoReturn, Optional, Union

import numpy as np
from PyQt5.Qt import QApplication, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from backend.cognitive_model import CognitiveModel
from main_window import Ui_MainWindow, _translate


def to_float(x: Any) -> Union[None, float]:
    try:
        return float(x)
    except ValueError:
        return None


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent: Optional[Any] = None):
        super(MainWindow, self).__init__(parent)

        try:
            self.default_adj_matrix = np.loadtxt("./data/ukraine.txt")
        except OSError:
            self.default_adj_matrix = np.ones((8, 8))
        self.row_count, self.col_count = self.default_adj_matrix.shape
        self.setupUi(self, self.col_count, self.row_count, self.default_adj_matrix)
        self.tableWidget.resizeColumnsToContents()

    def get_A(self) -> np.ndarray:
        A = []
        for i in range(self.tableWidget.rowCount()):
            A_row = []
            for j in range(self.tableWidget.columnCount()):
                val = to_float(self.tableWidget.item(i, j).text())
                if val is None:
                    return None
                A_row.append(val)
            A.append(np.array(A_row))
        return np.array(A)

    @pyqtSlot()
    def buildClicked(self) -> NoReturn:
        A = self.get_A()
        if A is None:
            QMessageBox.warning(self, "Error", "Error parsing matrix")
        else:
            cognitiveModel = CognitiveModel(A)
            cognitiveModel.draw_graph()

    def cycle_str(self, x: List[int]) -> str:
        return " - ".join(self.tableWidget.verticalHeaderItem(y).text() for y in x)

    @pyqtSlot()
    def researchClicked(self) -> NoReturn:
        A = self.get_A()
        if A is None:
            QMessageBox.warning(self, "Error", "Error parsing matrix")

        # researching A
        cognitiveModel = CognitiveModel(A)
        results = "Власні числа: \n"
        results += "\n".join(str(x) for x in cognitiveModel.calculate_eigenvalues())
        results += "\n"

        results += "Стійкість за збуренням: "
        results += "Так" if cognitiveModel.check_perturbation_stability() else "Ні"
        results += "\n"

        results += "Стійкість за значенням: "
        results += "Так" if cognitiveModel.check_numerical_stability() else "Ні"
        results += "\n"

        results += "Структурна стійкість: "
        cycles = cognitiveModel.check_structural_stability()
        if not cycles:
            results += "Так"
        else:
            results += "Ні, отримали наступні цикли: \n"
            for cycle in cycles:
                results += "(" + self.cycle_str(cycle) + ") \n"
        cognitiveModel.impulse_model()
        self.label.setText(results)

    @pyqtSlot()
    def openClicked(self) -> NoReturn:
        filename = QFileDialog.getOpenFileName(self, "Відкрити файл з данними", ".", "Data file (*.txt)")
        if filename != "":
            self.openLineEdit.setText(filename[0])
            df = np.loadtxt(filename[0])
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
                    item.setText(_translate("MainWindow", str(df[i, j]), None))
                    self.tableWidget.setItem(i, j, item)

            self.tableWidget.resizeColumnsToContents()

    @pyqtSlot()
    def addClicked(self) -> NoReturn:

        name = str(self.tableWidget.rowCount() + 1)
        r = self.tableWidget.rowCount()
        self.tableWidget.setColumnCount(r + 1)
        self.tableWidget.setRowCount(r + 1)
        self.tableWidget.setHorizontalHeaderItem(r, QTableWidgetItem(name))
        self.tableWidget.setVerticalHeaderItem(r, QTableWidgetItem(name))

        for i in range(r + 1):
            item = "0.0"
            self.tableWidget.setItem(i, r, QTableWidgetItem(item))
            self.tableWidget.setItem(r, i, QTableWidgetItem(item))

        self.tableWidget.resizeColumnsToContents()

    @pyqtSlot()
    def removeClicked(self) -> NoReturn:
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


def main() -> NoReturn:
    app = QApplication(sys.argv)
    app.setApplicationName("Work 8")
    mainWindow = MainWindow()
    mainWindow.setWindowTitle("Когнітивне моделювання")
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
