import inspect

from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class StockAPI(QAxWidget):
    def __init__(self):
        super().__init__()

    def connectStock(self):
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self._comm_connect()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        # server connect 관련 event 발생 시 callback
        self.OnEventConnect.connect(self._event_connect)
        # self.OnReceiveTrData.connect(self._receive_tr_data)

    def _comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_market_code(self):
        # GetCodeListByMarket 으로 종목코드 요청
        #result = self.kiwoom.dynamicCall('GetCodeListByMarket(QString)', ['0'])
        result = self.dynamicCall("GetCodeListByMarket(QString)", ["0"])
        return result
        code_list = result.split(';')
        return code_list

    def GetLoginInfo(self, tag):
        return self.dynamicCall("GetLoginInfo(QString)", [tag])

    def get_code_data(self, code, date):
        print('start', inspect.stack()[0][3], code, date)
        self.SetInputValue("종목코드", code)
        self.SetInputValue("기준일자", date)
        self.SetInputValue("수정주가구분", 1)
        self.CommRqData("opt10081_req", "opt10081", 0, "0101")
        print('end', inspect.stack()[0][3], code, date)

    def SetInputValue(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def commKwRqData(self, arrCode, next, codeCount, typeFlag, rQName, screenNo):
        self.dynamicCall("CommKwRqData(QString, QBoolean, int, int, QString, QString)", arrCode, next, codeCount, typeFlag, rQName, screenNo)

    def CommRqData(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        #self.tr_event_loop = QEventLoop()
        #self.tr_event_loop.exec_()

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10081_full(self, rqname, trcode):
        data_cnt = self.GetRepeatCnt(trcode, rqname)

        for i in range(data_cnt):
            date = self.CommGetData(trcode, "", rqname, i, "일자")
            open = self.CommGetData(trcode, "", rqname, i, "시가")
            high = self.CommGetData(trcode, "", rqname, i, "고가")
            low = self.CommGetData(trcode, "", rqname, i, "저가")
            close = self.CommGetData(trcode, "", rqname, i, "현재가")
            volume = self.CommGetData(trcode, "", rqname, i, "거래량")
            print(date, open, high, low, close, volume)

    def _opt10081(self, rqname, trcode):
        data_cnt = self.GetRepeatCnt(trcode, rqname)
        i=0
        date = self.CommGetData(trcode, "", rqname, i, "일자")
        open = self.CommGetData(trcode, "", rqname, i, "시가")
        high = self.CommGetData(trcode, "", rqname, i, "고가")
        low = self.CommGetData(trcode, "", rqname, i, "저가")
        close = self.CommGetData(trcode, "", rqname, i, "현재가")
        volume = self.CommGetData(trcode, "", rqname, i, "거래량")
        print(date, open, high, low, close, volume)

    def CommGetData(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code, real_type, field_name, index, item_name)
        return ret.strip()

    def GetCommData(self, code, field_name, index, item_name):
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString)", code, field_name, index, item_name)
        return ret.strip()

    def GetRepeatCnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def SetRealReg(self, screen_no, code_list, fid_list, real_type):
        # todo, screen_no should be 4 digits
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", screen_no, code_list, fid_list, real_type)

    def DisConnectRealData(self, screen_no):
        self.dynamicCall("DisConnectRealData(QString)", screen_no)

    def GetCommRealData(self, code, fid):
        data = self.dynamicCall("GetCommRealData(QString, int)", code, fid)
        return data

    def SendOrder(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    def GetChejanData(self, fid):
        '''
        FID	설명
        9203	주문번호
        302	종목명
        900	주문수량
        901	주문가격
        902	미체결수량
        904	원주문번호
        905	주문구분
        908	주문/체결시간
        909	체결번호
        910	체결가
        911	체결량
        10	현재가, 체결가, 실시간종가
        '''
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret