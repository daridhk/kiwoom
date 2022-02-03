import sys
import datetime
import time

from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QCoreApplication, QDateTime, Qt, QObject, pyqtSlot, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import uic
'''
at pyCharm terminal, 
python -m PyQt5.uic.pyuic -x tableWidget.ui -o tableWidget.py
'''
import StockAPI
# from Worker import Worker
from tableWidget import *
import stock_config

COL_NAME = 0
COL_CHANGE_YN = 1
COL_SELL_YN = 2
#COL_BUGDGT = 1
COL_STEP = 3
COL_BALANCE = 4
COL_PURCHASE_PRICE = 5
COL_MARKET = 6
COL_QUANTITY = 7
COL_TARGET_PERCENT = 8
COL_YIELD = 8
COL_GOSTOP = 9
COL_PERIOD = 10

INDEX_TARGET_YIELD = 0
INDEX_SELL_PERCENT = 1


class async_signal(QObject):
    obj = pyqtSignal()

    def __init__(self):
        super().__init__()

    def emit(self):
        self.obj.emit()

    def connect(self, action):
        self.obj.connect(action)

class MyWindow(Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btnStart.clicked.connect(self.start_transaction)
        self.btnStop.clicked.connect(self.stop_transaction)

        self.btnClose.clicked.connect(QCoreApplication.instance().quit)

        self.btnSell.hide()
        # self.btnBuy.hide()
        #self.btnSell.clicked.connect(self.sell_transaction)
        self.btnBuy.clicked.connect(self.buy_transaction)

        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)

        #self.chbox = QCheckBox()
        #self.tableWidget.setCellWidget(0,1, self.chbox)
        self.stock_api = StockAPI.StockAPI()
        self.stock_api.connectStock()
        self.stock_api.OnReceiveRealData.connect(self._handler_real_data)
        self.stock_api.OnReceiveTrData.connect(self._handler_tr_data)
        self.stock_api.OnReceiveChejanData.connect(self._handler_chejan_data)
        self.stock_api.OnReceiveMsg.connect(self._handler_receive_msg)

        self.codes, self.plans, self.leave, self.asset = stock_config.StockConfig().load_config()

        self.screen_nubmer_get_balance = "0010"
        # self.get_market_price_screen_number = 1
        self.screen_number_market_price = "0001"

        # self.balance_signal = async_signal()
        # self.balance_signal.connect(self.async_get_balance)

        '''
        self.worker = Worker(self)
        self.worker_table_update = False
        self.worker_start = False
        self.worker_sleep = 2
        self.worker.start()
        '''

        self.timer_period = 1000
        self.timer_count = 0
        self.timer_worker = QTimer(self)
        self.timer_worker.setInterval(self.timer_period)
        self.timer_worker.timeout.connect(self.timer_worker_sell)

        self.start_update()

    def _handler_tr_data(self, screen_no, rqname, trcode, record_name, next):
        print('_handler_tr_data', screen_no, rqname, trcode, record_name, next)
        '''
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False
        '''
        if rqname == 'commKwRqData':
            self._commKwRqData(rqname, trcode)
        elif rqname == "계좌평가잔고내역요청":
            self._handler_get_balance(rqname, trcode, next)
        if rqname == "예수금상세현황요청":
            self._handler_get_cash(rqname, trcode)
        elif rqname == 'send_order_req':
            print('rqname == send_order_req')
            self.sell_transaction_event_loop.exit()

    def _handler_get_cash(self, sRQName, sTrCode):
        deposit = self.stock_api.GetCommData(sTrCode, sRQName, 0, "예수금")
        self.deposit = int(deposit)
        withdraw_deposit = self.stock_api.GetCommData(sTrCode, sRQName, 0, "출금가능금액")
        self.withdraw_deposit = int(withdraw_deposit)
        order_deposit = self.stock_api.GetCommData(sTrCode, sRQName, 0, "주문가능금액")
        self.order_deposit = int(order_deposit)
        #self.cancel_screen_number(self.screen_my_account)
        #self.get_deposit_loop.exit()

    def get_balance(self, nPrevNext=0):
        print('_get_account_evaluation_balance started', nPrevNext)
        self.stock_api.SetInputValue("계좌번호", self.account_number)
        print('_get_account_evaluation_balance started middle 1')
        self.stock_api.SetInputValue("비밀번호", " ")
        self.stock_api.SetInputValue("비밀번호입력매체구분", "00")
        self.stock_api.SetInputValue("조회구분", "1")
        print('_get_account_evaluation_balance started middle 2')
        '''
        if self.screen_nubmer_get_balance == "10":
            self.screen_nubmer_get_balance = "11"
        else:
            self.screen_nubmer_get_balance = "10"
        '''
        res = self.stock_api.CommRqData("계좌평가잔고내역요청", "opw00018", nPrevNext, self.screen_nubmer_get_balance)
        print('result CommRqData = ', res)
        if nPrevNext==0:
            self.get_balance_event_loop = QtCore.QEventLoop()
            print('self.get_balance_event_loop.exec_()')
            self.get_balance_event_loop.exec_()
        else:
            print('get_balance nPrevNext = ', nPrevNext)

    def _handler_get_balance(self, sRQName, sTrCode, sPrevNext=0):
        print('_handler_get_balance started')
        total_buy_money = self.stock_api.GetCommData(sTrCode, sRQName, 0, "총매입금액")
        self.total_sell_money = int(total_buy_money)
        total_evaluation_money = self.stock_api.GetCommData(sTrCode, sRQName, 0, "총평가금액")
        self.total_evaluation_money = int(total_evaluation_money)
        total_evaluation_profit_and_loss_money = self.stock_api.GetCommData(sTrCode, sRQName, 0, "총평가손익금액")
        self.total_evaluation_profit_and_loss_money = int(total_evaluation_profit_and_loss_money)

        total_yield = self.stock_api.GetCommData(sTrCode, sRQName, 0, "총수익률(%)")
        self.total_yield = float(total_yield)

        #print(total_buy_money, total_evaluation_money, total_evaluation_profit_and_loss_money)

        cnt = self.stock_api.GetRepeatCnt(sTrCode, sRQName)

        for i in range(cnt):
            stock_code = self.stock_api.GetCommData(sTrCode, sRQName, i, "종목번호")
            stock_code = stock_code.strip()[1:]
            stock_name = self.stock_api.GetCommData(sTrCode, sRQName, i, "종목명")
            stock_name = stock_name.strip()
            stock_evaluation_profit_and_loss = self.stock_api.GetCommData(sTrCode, sRQName, i, "평가손익")
            stock_evaluation_profit_and_loss = int(stock_evaluation_profit_and_loss)
            stock_yield = self.stock_api.GetCommData(sTrCode, sRQName, i, "수익률(%)")
            stock_yield = float(stock_yield)
            stock_buy_money = self.stock_api.GetCommData(sTrCode, sRQName, i, "매입가")
            stock_buy_money = int(stock_buy_money)
            stock_quantity = self.stock_api.GetCommData(sTrCode, sRQName, i, "보유수량")
            stock_quantity = int(stock_quantity)
            stock_trade_quantity = self.stock_api.GetCommData(sTrCode, sRQName, i, "매매가능수량")
            stock_trade_quantity = int(stock_trade_quantity)

            stock_present_price = self.stock_api.GetCommData(sTrCode, sRQName, i, "현재가")
            stock_present_price = int(stock_present_price)

            print('종목', stock_code, stock_name, stock_evaluation_profit_and_loss, stock_yield, stock_buy_money, stock_quantity, stock_trade_quantity, stock_present_price)
            self.asset[stock_code]['name'] = stock_name
            self.asset[stock_code]['purchase_price'] = stock_buy_money
            self.asset[stock_code]['quantity'] = stock_quantity
            self.asset[stock_code]['market'] = stock_present_price

            '''
            self.asset[code] = {'index': i, 'code': code, 'name': name, 'price': market_price}
            self.tableWidget.setItem(self.asset[code]['index'], 0, QTableWidgetItem(self.asset[code]['code']))
            self.tableWidget.setItem(self.asset[code]['index'], 1, QTableWidgetItem(self.asset[code]['name']))
            self.tableWidget.setItem(self.asset[code]['index'], 2, QTableWidgetItem(self.asset[code]['price']))
            '''
            #print(self.asset[stock_code])

        if sPrevNext == "2":
            self.get_balance("2")
        else:
            self.get_balance_event_loop.exit()
            print('self.get_balance_event_loop.exit()')

        #else:
        #    self.cancel_screen_number(self.screen_my_account)
        #    self.get_account_evaluation_balance_loop.exit()
        print('end of item list')

    def _commKwRqData(self, rqname, trcode):
        print('_commKwRqData start')
        data_cnt = self.stock_api.GetRepeatCnt(trcode, rqname)
        for i in range(data_cnt):
            code = self.stock_api.GetCommData(trcode, rqname, i, "종목코드")
            name = self.stock_api.GetCommData(trcode, rqname, i, "종목명")
            market_price = self.stock_api.GetCommData(trcode, rqname, i, "현재가")
            '''
            code = self.stock_api.CommGetData(trcode, "", rqname, i, "종목코드")
            name = self.stock_api.CommGetData(trcode, "", rqname, i, "종목명")
            market_price = self.stock_api.CommGetData(trcode, "", rqname, i, "현재가")
            '''
            # stock_present_price = self.stock_api.GetCommData(sTrCode, sRQName, i, "현재가")
            self.asset[code]['name'] = name
            self.asset[code]['market'] = market_price

        self.market_price_event_loop.exit()
        print('self.market_price_event_loop.exit()')

    def _start_real_time_market_price(self):
        for index, code in enumerate(self.codes):
            print('_start_real_time_market_price', index, code)
            self.stock_api.SetRealReg(str(index), code, "20;10", 0)

    def _handler_real_data(self, code, real_type, data):
        if real_type == "주식체결":
            # self.get_balance()
            # 체결 시간
            time = self.stock_api.GetCommRealData(code, 20)
            # 현재가
            price = self.stock_api.GetCommRealData(code, 10)
            date = datetime.datetime.now().strftime("%Y-%m-%d ")
            time = datetime.datetime.strptime(date + time, "%Y-%m-%d %H%M%S")
            print(time, code, price)
            self.asset[code]['change_yn'] = 'Y'
            self.asset[code]['market'] = price
            self._setTable(self.asset[code]['index'], COL_CHANGE_YN, 'Y')
            self._setTable(self.asset[code]['index'], COL_MARKET, price)
            # self.sell_logic()
            # self.sell_item(code, self.asset[code]['purchase_price'], price)

        # self.enable_all_button()

    def _handler_chejan_data(self, gubun, item_cnt, fid_list):
        print('_handler_chejan_data', gubun, item_cnt, fid_list)
        print(self.stock_api.GetChejanData(9203), self.stock_api.GetChejanData(302), self.stock_api.GetChejanData(900), self.stock_api.GetChejanData(901))


    def _handler_receive_msg(self, scr_no, rq_name, tr_code, msg):
        # print("receive_msg, rq_name = " + rq_name + ", tr_code = " + tr_code + ", msg = " + msg)
        self.enable_all_button()

    def _get_account(self):
        account_num = self.stock_api.GetLoginInfo('ACCNO')
        account_num = account_num.split(';')[0]
        # print(account_num)
        return account_num
        # == 8011118411;

    def get_market_price(self):
        code_chain = ';'.join(self.codes)
        '''
        self.get_market_price_screen_number += 1
        if self.get_market_price_screen_number>200:
            self.get_market_price_screen_number = 1
        screen_number = '%04d' % self.get_market_price_screen_number
        print('screen number = ', screen_number)
        self.stock_api.commKwRqData(code_chain, False, len(self.codes), 0, 'commKwRqData', screen_number)
        '''
        self.stock_api.commKwRqData(code_chain, False, len(self.codes), 0, 'commKwRqData', self.screen_number_market_price)
        self.market_price_event_loop= QtCore.QEventLoop()
        print('self.market_price_event_loop.exec_()')
        self.market_price_event_loop.exec_()


    def start_update(self):
        # self.disable_all_button()
        # self.btnStart.setEnabled(False)

        print('start_update')
        self.account_number = self._get_account()
        # self.worker_start = not True

        self.get_balance()
        self.get_market_price()

        print('asset ----------------------')
        for code in self.codes:
            print(self.asset[code])
        self._fill_table()
        stock_config.StockConfig().save_config(self.codes, self.plans, self.leave, self.asset)
        self._fill_plans()

        time.sleep(1)
        self._start_real_time_market_price()

    def start_transaction(self):
        print('start_transaction')
        self.timer_worker.start()

    def stop_transaction(self):
        print('stop_transaction')
        self.timer_worker.stop()

    def _fill_table(self):
        for index, code in enumerate(self.codes):
            asset = self.asset[code]
            self._setTable(index, COL_NAME, code+'('+asset['name']+')')
            # self._setTable(index, COL_NAME, code + '(' + 'oooo' + ')')
            self._setTable(index, COL_CHANGE_YN, asset['change_yn'])
            self._setTable(index, COL_SELL_YN, asset['sell_yn'])
            # self._setTable(index, COL_BUGDGT, asset['t_budget'])
            self._setTable(index, COL_STEP, asset['step'])
            self._setTable(index, COL_BALANCE, int(asset['market'])*int(asset['quantity']))
            self._setTable(index, COL_PURCHASE_PRICE, asset['purchase_price'])
            self._setTable(index, COL_MARKET, asset['market'])
            self._setTable(index, COL_QUANTITY, asset['quantity'])
            #self._setTable(index, COL_TARGET_PERCENT, asset['target_percent'])
            self._setTable(index, COL_YIELD, asset['yield']*100.0)
            self._setTable(index, COL_GOSTOP, asset['gostop'])
            self._setTable(index, COL_PERIOD, asset['period'])
            #purchase_price':0, 'quantity':0, 'market_price':0, 'target_percent': 0.1, 'yield': 0, 'gostop': True, 'period': 24}

    def _setTable(self, row, col, value):
        self.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

    def _fill_plans(self):
        for index, plan in enumerate(self.plans):
            self._setPlan(index, 0, plan[0])
            self._setPlan(index, 1, plan[1])

    def _setPlan(self, row, col, value):
        self.tableTarget.setItem(row, col, QTableWidgetItem(str(value)))

    '''
    def sell_transaction(self):
        self.disable_all_button()
        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        account = self.account_number
        # account = '8011118411'
        order_type = 2
        code = self.codes[2]
        hoga = '03'
        num = 10
        price = 100

        print('sell_transaction', "send_order_req", "21", account, order_type, code, num, price, hoga, "")
        self.stock_api.SendOrder("send_order_req", "21", account, order_type, code, num, price, hoga, "")
        self.sell_transaction_event_loop= QtCore.QEventLoop()
        self.sell_transaction_event_loop.exec_()
    '''
    def buy_transaction(self):
        self.disable_all_button()
        print('buy_transaction')

        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        account = self.account_number
        # account = '8011118411'
        order_type = 1
        code = self.codes[3]
        hoga = '03'
        num = 14
        price = 100

        print('buy_transaction', "send_order_req", "20", account, order_type, code, num, price, hoga, "")
        self.stock_api.SendOrder("send_order_req", "20", account, order_type, code, num, price, hoga, "")
        self.sell_transaction_event_loop= QtCore.QEventLoop()
        self.sell_transaction_event_loop.exec_()

    def enable_all_button(self):
        # self.btnSell.setEnabled(True)
        # self.btnBuy.setEnabled(True)
        # self.btnStart.setEnabled(True)
        self.btnClose.setEnabled(True)

    def disable_all_button(self):
        # self.btnSell.setEnabled(False)
        # self.btnBuy.setEnabled(False)
        # self.btnStart.setEnabled(False)
        self.btnClose.setEnabled(False)

    def sell_item(self, code, purchase, price):
        if self.asset[code]['quantity'] > 0:
            step = self.asset[code]['step']
            sellYN, next_step, sell_percent = self.meet_sell_condition(step, purchase, price)
            if sellYN:
                self._update_column(code, COL_SELL_YN, 'sell_yn', 'Y')
            else:
                self._update_column(code, COL_SELL_YN, 'sell_yn', 'N')

            if sellYN:
                self.asset[code]['step'] = next_step
                sell_quantity = self.get_sell_quantity(code, sell_percent)
                self.sell_item_transaction(code, sell_quantity)
                self.get_balance()
                self._fill_table()
                stock_config.StockConfig().save_config(self.codes, self.plans, self.leave, self.asset)

    '''
    def async_get_balance(self):
        print("signal async_get_balance .... ")
        print('timer signal async_get_balance :', self.timer_count)
        self.timer_count += 1
        self.get_balance()
        self._fill_table()
        # stock_config.StockConfig().save_config()
    '''

    def timer_worker_sell(self):
        print('doing timer_worker_sell +++++++++++')
        for code in self.codes:
            self._update_column(code, COL_SELL_YN, 'sell_yn', '.')
            if self.asset[code]['change_yn'] == 'Y':
                self.sell_item(code, self.asset[code]['purchase_price'], self.asset[code]['market'])
                self._update_column(code, COL_CHANGE_YN, 'change_yn', '.')

    def _update_column(self, code, column, dic_column, value):
        self.asset[code][dic_column] = value
        self._setTable(self.asset[code]['index'], column, self.asset[code][dic_column])

    def meet_sell_condition(self, step, purchase, price):
        purchase = abs(int(purchase))
        price = abs(int(price))
        if purchase <= 1:
            return False, 0, 0
        profit = (price-purchase)*100/purchase
        if profit <= 0:
            return False, 0, 0
        next_step = len(self.plans) - 1
        while next_step >= step:
            if profit > self.plans[next_step][INDEX_TARGET_YIELD]:
                return True, next_step+1, self.plans[next_step][INDEX_SELL_PERCENT]
            next_step -= 1
        return False, 0, 0

        '''
        for next_step, plan in reversed(list(enumerate(self.plans))):
            if next_step >= step and profit > plan[INDEX_TARGET_YIELD]:
                return True, next_step+1, plan[INDEX_SELL_PERCENT]
        return False, 0, 0
        '''

    def get_sell_quantity(self, code, sell_percent):
        current_quantity = self.asset[code]['quantity']
        sell_quantity = int(current_quantity*sell_percent/100)
        return sell_quantity

    def sell_item_transaction(self, code, sell_quantity):
        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        account = self.account_number
        order_type = order_type_lookup['신규매도']
        hoga = hoga_lookup['시장가']

        # price is not used
        price = 100000000

        print('sell_item_transaction', "send_order_req", "21", account, order_type, code, sell_quantity, price, hoga, "")
        error_code = self.stock_api.SendOrder("send_order_req", "21", account, order_type, code, sell_quantity, price, hoga, "")
        if error_code != 0:
            print("error = ", error_code)
        self.sell_transaction_event_loop= QtCore.QEventLoop()
        self.sell_transaction_event_loop.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

