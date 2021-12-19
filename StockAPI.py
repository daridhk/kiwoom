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
        self.set_input_value("종목코드", code)
        self.set_input_value("기준일자", date)
        self.set_input_value("수정주가구분", 1)
        self.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        print('end', inspect.stack()[0][3], code, date)


    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

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
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")
            print(date, open, high, low, close, volume)

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)
        i=0
        date = self._comm_get_data(trcode, "", rqname, i, "일자")
        open = self._comm_get_data(trcode, "", rqname, i, "시가")
        high = self._comm_get_data(trcode, "", rqname, i, "고가")
        low = self._comm_get_data(trcode, "", rqname, i, "저가")
        close = self._comm_get_data(trcode, "", rqname, i, "현재가")
        volume = self._comm_get_data(trcode, "", rqname, i, "거래량")
        print(date, open, high, low, close, volume)

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
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
