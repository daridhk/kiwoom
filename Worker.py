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
        # self.items = stock_config.StockConfig().get_items()

    def run(self):
        count = 0
        while True:
            if self.parent.worker_start:
                now = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
                print(now, 'worker : start work ', count)
                count += 1

                # self.parent.get_balance()
                self.parent.balance_signal.emit()
                # self.parent.get_market_price()
                # test -- self.parent.sell_item('000270', 90000, 19000)
                # self.parent._fill_table()
                # self.parent._fill_plans()
                # now = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
                # print(now, 'worker : end')

            now = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
            # print(now, 'worker is running')
            time.sleep(self.parent.worker_sleep)

