import time
import datetime
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
import stock_config
import StockAPI

class Worker(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.items = stock_config.StockConfig().get_items()

    def run(self):
        names = {}
        for item in self.items:
            names[item] = self.parent.stock_api.get_name(item)+' ('+item+')'
            print(names[item])
        # codes = ';'.join(self.items)
        # res = self.parent.stock_api.get_market_data(codes, len(self.items))
        today = datetime.date.today().strftime('%Y%m%d')
        print(today)
        while True:
            for index, item in enumerate(self.items):
                print(index, item)
                self.parent.stock_api.get_code_data(item, today)
                self.parent.tableWidget.setItem(index, 0, QTableWidgetItem(names[item]))
                self.parent.lineEdit.setText(names[item])
                time.sleep(1)

