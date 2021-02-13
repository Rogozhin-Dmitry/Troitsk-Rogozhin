import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.tableWidget.setColumnCount(len(self.cur.execute("SELECT * FROM coffee").fetchone()))
        self.tableWidget.setHorizontalHeaderLabels([description[0] for description in self.cur.description])
        self.view_result()

    def view_result(self):
        res = self.cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(res))
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())