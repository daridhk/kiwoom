import time

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *


class Worker(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        i = 0
        while True:
            for row in range(10):
                for col in range(10):
                    val = i+row*10+col
                    self.parent.tableWidget.setItem(row, col, QTableWidgetItem(str(val)))
                    self.parent.lineEdit.setText(str(val))
                    time.sleep(0.3)
            #self.parent.tableWidget.item(0,0).setText(str(i))

            # self.parent.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            i += 1

