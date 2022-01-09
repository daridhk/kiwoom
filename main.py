import sys
import time
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QCoreApplication, QDateTime, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import uic
'''
at pyCharm terminal, 
python -m PyQt5.uic.pyuic -x tableWidget.ui -o tableWidget.py
'''
import StockAPI
from Worker import Worker
from tableWidget import *
import stock_config

COL_NAME = 0
COL_BUGDGT = 1
COL_STEP = 2
COL_BALANCE = 3
COL_PURCHASE_PRICE = 4
COL_MARKET = 5
COL_TARGET_PERCENT = 6
COL_YIELD = 7
COL_GOSTOP = 8
COL_PERIOD = 9


'''
Form_class, Window_class = uic.loadUiType("tableWidget.ui")

class MyWindow2(Form_class, Window_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnStart.setEnabled(False)
'''

class MyWindow(Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btnStart.clicked.connect(self.start_transaction)
        self.btnStop.clicked.connect(self.stop_transaction)

        self.btnClose.clicked.connect(QCoreApplication.instance().quit)

        self.btnSell.clicked.connect(self.sell_transaction)
        self.btnBuy.clicked.connect(self.buy_transaction)

        self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)

        #self.chbox = QCheckBox()
        #self.tableWidget.setCellWidget(0,1, self.chbox)
        self.stock_api = StockAPI.StockAPI()
        self.stock_api.connectStock()
        self.stock_api.OnReceiveRealData.connect(self._handler_real_data)
        self.stock_api.OnReceiveTrData.connect(self._handler_tr_data)
        self.stock_api.OnReceiveChejanData.connect(self._handler_chejan_data)
        self.stock_api.OnReceiveMsg.connect(self._handler_receive_msg)

        self.codes = stock_config.StockConfig().get_codes()
        self.asset = stock_config.StockConfig().load_settings(self.codes)
        # print(self.asset)


    def _handler_tr_data(self, screen_no, rqname, trcode, record_name, next):
        # print('_handler_tr_data', screen_no, rqname, trcode, record_name, next)
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

    def _handler_get_cash(self, sRQName, sTrCode):
        deposit = self.stock_api.GetCommData(sTrCode, sRQName, 0, "예수금")
        self.deposit = int(deposit)
        withdraw_deposit = self.stock_api.GetCommData(sTrCode, sRQName, 0, "출금가능금액")
        self.withdraw_deposit = int(withdraw_deposit)
        order_deposit = self.stock_api.GetCommData(sTrCode, sRQName, 0, "주문가능금액")
        self.order_deposit = int(order_deposit)
        #self.cancel_screen_number(self.screen_my_account)
        #self.get_deposit_loop.exit()

    def _get_balance(self, nPrevNext=0):
        # print('_get_account_evaluation_balance started')
        self.stock_api.SetInputValue("계좌번호", self.account_number)
        self.stock_api.SetInputValue("비밀번호", " ")
        self.stock_api.SetInputValue("비밀번호입력매체구분", "00")
        self.stock_api.SetInputValue("조회구분", "1")
        self.stock_api.CommRqData("계좌평가잔고내역요청", "opw00018", nPrevNext, "10")
        self.account_event_loop = QtCore.QEventLoop()
        self.account_event_loop.exec_()

    def _handler_get_balance(self, sRQName, sTrCode, sPrevNext=0):
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

            #print('종목', stock_code, stock_name, stock_evaluation_profit_and_loss, stock_yield, stock_buy_money, stock_quantity, stock_trade_quantity, stock_present_price)
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
            self._get_balance("2")
        else:
            self.account_event_loop.exit()
        #else:
        #    self.cancel_screen_number(self.screen_my_account)
        #    self.get_account_evaluation_balance_loop.exit()
        print('end of item list')

    def _commKwRqData(self, rqname, trcode):
        data_cnt = self.stock_api.GetRepeatCnt(trcode, rqname)
        for i in range(data_cnt):
            code = self.stock_api.CommGetData(trcode, "", rqname, i, "종목코드")
            name = self.stock_api.CommGetData(trcode, "", rqname, i, "종목명")
            market_price = self.stock_api.CommGetData(trcode, "", rqname, i, "현재가")

            self.asset[code]['name'] = name
            self.asset[code]['market'] = market_price

        #for code in self.codes:
        #    print(self.asset[code])
        self.market_price_event_loop.exit()

    def _start_real_time_market_price(self):
        for index, code in enumerate(self.codes):
            self.stock_api.SetRealReg(str(index), code, "20;10", 0)

    def _handler_real_data(self, code, real_type, data):
        if real_type == "주식체결":
            # 체결 시간
            time = self.stock_api.GetCommRealData(code, 20)
            # 현재가
            price = self.stock_api.GetCommRealData(code, 10)
            date = datetime.datetime.now().strftime("%Y-%m-%d ")
            time = datetime.datetime.strptime(date + time, "%Y-%m-%d %H%M%S")
            self.asset[code]['market'] = price
            self._setTable(self.asset[code]['index'], COL_MARKET, price)
            self.sell_logic()

        self.enable_all_button()

    def _handler_chejan_data(self, gubun, item_cnt, fid_list):
        print('_handler_chejan_data', gubun, item_cnt, fid_list)
        print(self.stock_api.GetChejanData(9203), self.stock_api.GetChejanData(302), self.stock_api.GetChejanData(900), self.stock_api.GetChejanData(901))
        self.enable_all_button()

    def _handler_receive_msg(self, scr_no, rq_name, tr_code, msg):
        # print("receive_msg, rq_name = " + rq_name + ", tr_code = " + tr_code + ", msg = " + msg)
        self.enable_all_button()

    def _get_account(self):
        account_num = self.stock_api.GetLoginInfo('ACCNO')
        account_num = account_num.split(';')[0]
        # print(account_num)
        return account_num
        # == 8011118411;

    def _get_market_price(self):
        code_chain = ';'.join(self.codes)
        self.stock_api.commKwRqData(code_chain, False, len(self.codes), 0, 'commKwRqData', '1')
        self.market_price_event_loop= QtCore.QEventLoop()
        self.market_price_event_loop.exec_()


    def start_transaction(self):
        self.disable_all_button()
        print('start_transaction')
        # self.worker = Worker(self)
        # self.worker.start()

        self.account_number = self._get_account()

        print('waiting for _get_account_balance() completes ----------------------')
        self._get_balance()

        self._get_market_price()

        print('asset ----------------------')
        for code in self.codes:
            print(self.asset[code])

        self._fill_table()

        self._start_real_time_market_price()

        self.enable_all_button()

        #for index, code in enumerate(self.codes):
        #    self.stock_api.SetRealReg(str(index), code, "20;10", 0)

        #self.stock_api.SetRealReg(self.codes[0], self.codes[0], "20;10", 0)

    def _fill_table(self):
        for index, code in enumerate(self.codes):
            asset = self.asset[code]
            self._setTable(index, COL_NAME, code+'('+asset['name']+')')
            self._setTable(index, COL_BUGDGT, asset['t_budget'])
            self._setTable(index, COL_STEP, asset['step'])
            # self._setTable(index, COL_BALANCE, str(int(asset['market'])*int(asset['quantity'])))
            self._setTable(index, COL_PURCHASE_PRICE, asset['purchase_price'])
            self._setTable(index, COL_MARKET, asset['market'])
            self._setTable(index, COL_TARGET_PERCENT, asset['target_percent'])
            self._setTable(index, COL_YIELD, asset['yield'])
            self._setTable(index, COL_GOSTOP, asset['gostop'])
            self._setTable(index, COL_PERIOD, asset['period'])
            #purchase_price':0, 'quantity':0, 'market_price':0, 'target_percent': 0.1, 'yield': 0, 'gostop': True, 'period': 24}

    def _setTable(self, row, col, value):
        self.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

    def stop_transaction(self):
        # self.worker.terminate()
        print('stop_transaction')
        for code in self.codes:
            self.stock_api.DisConnectRealData(code)

    def sell_transaction(self):
        self.disable_all_button()
        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        # account = self.account_number
        account = '8011118411'
        order_type = 2
        code = self.codes[2]
        hoga = '03'
        num = 10
        price = 100

        print('sell_transaction', "send_order_req", "21", account, order_type, code, num, price, hoga, "")
        self.stock_api.SendOrder("send_order_req", "21", account, order_type, code, num, price, hoga, "")

    def buy_transaction(self):
        self.disable_all_button()
        print('buy_transaction')

        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        # account = self.account_number
        account = '8011118411'
        order_type = 1
        code = self.codes[2]
        hoga = '03'
        num = 7
        price = 100

        print('sell_transaction', "send_order_req", "20", account, order_type, code, num, price, hoga, "")
        self.stock_api.SendOrder("send_order_req", "20", account, order_type, code, num, price, hoga, "")

    def enable_all_button(self):
        self.btnSell.setEnabled(True)
        self.btnBuy.setEnabled(True)
        self.btnStart.setEnabled(True)


    def disable_all_button(self):
        self.btnSell.setEnabled(False)
        self.btnBuy.setEnabled(False)
        self.btnStart.setEnabled(False)

    def sell_logic(self):
        print('do sell logic')

    def buy_logic(self):
        print('buy logic')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
