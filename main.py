import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox


class MyWidget_1(QDialog):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.parent = parent
        self.pushButton.clicked.connect(self.new_result)

    def show(self):
        super().show()
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')
        self.comboBox.setCurrentIndex(0)

    def new_result(self):
        self.parent.cur.execute(f'INSERT INTO coffee VALUES ((SELECT MAX(id) FROM coffee)+1, "{self.lineEdit.text()}",'
                                + f' "{self.lineEdit_2.text()}", {self.lineEdit_3.text()},'
                                + f' "{str(self.comboBox.currentText()).capitalize()}", "{self.lineEdit_4.text()}",'
                                + f' {self.lineEdit_5.text()}, {self.lineEdit_6.text()})')
        self.parent.con.commit()
        self.parent.view_result()
        self.hide()


class MyWidget_2(QDialog):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.parent = parent
        self.pushButton.clicked.connect(self.new_result)

    def show(self):
        super().show()
        self.lineEdit.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 1).text())
        self.lineEdit_2.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 2).text())
        self.lineEdit_3.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 3).text())
        self.lineEdit_4.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 5).text())
        self.lineEdit_5.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 6).text())
        self.lineEdit_6.setText(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 7).text())
        self.comboBox.setCurrentIndex(
            int(not bool(self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 4).text())))

    def new_result(self):
        self.parent.cur.execute(f'UPDATE coffee SET name="{self.lineEdit.text()}", type="{self.lineEdit_2.text()}", '
                                + f'degree_of_roast={self.lineEdit_3.text()},'
                                + f' grind="{str(self.comboBox.currentText()).capitalize()}",'
                                + f' description="{self.lineEdit_4.text()}",'
                                + f' price={self.lineEdit_5.text()}, packaging={self.lineEdit_5.text()}'
                                + f' WHERE id=' +
                                self.parent.tableWidget.item(self.parent.tableWidget.currentRow(), 0).text())
        self.parent.con.commit()
        self.parent.view_result()
        self.hide()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.tableWidget.setColumnCount(len(self.cur.execute("SELECT * FROM coffee").fetchone()))
        self.tableWidget.setHorizontalHeaderLabels([description[0] for description in self.cur.description])
        self.view_result()

        self.new_file = MyWidget_1(self)
        self.editor = MyWidget_2(self)
        self.pushButton.clicked.connect(lambda: self.new_file.show())
        self.pushButton_2.clicked.connect(self.open_editor)

    def view_result(self):
        res = self.cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(res))
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def open_editor(self):
        if self.tableWidget.currentRow() != -1:
            self.editor.show()
        else:
            QMessageBox.question(self, '', "Выберите элемент для изменения", QMessageBox.Ok)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
