from PyQt5.QAxContainer import *

class KiwoomAPI:
    def __init__(self, connect=1):
        self.connectKiwoom(connect)

    def connectKiwoom(self, connect=1):
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        if connect == 1:
            # API 연결
            self.kiwoom.dynamicCall("CommConnect()")

    def get_market_code(self):
        # GetCodeListByMarket 으로 종목코드 요청
        #result = self.kiwoom.dynamicCall('GetCodeListByMarket(QString)', ['0'])
        result = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
        return result
        code_list = result.split(';')
        return code_list

    def get_name(self, code):
        name = self.kiwoom.dynamicCall('GetMasterCodeName(QString)', code)
        return name
