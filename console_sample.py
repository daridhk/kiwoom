import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *
import time

from PyQt5.QAxContainer import QAxWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()


class KiwoomAPI:
    def __init__(self):
        self.OCXconn = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

    def login(self):
        ret = self.OCXconn.dynamicCall("CommConnect()")
        print(ret)

    def btn1_clicked(self):
        ret = self.OCXconn.dynamicCall("GetCodeListByMarket(QString)", ["0"])
        print(ret)
        kospi_code_list = ret.split(';')
        kospi_code_name_list = []

        for x in kospi_code_list:
            name = self.OCXconn.dynamicCall("GetMasterCodeName(QString)", [x])
            kospi_code_name_list.append(x + " : " + name)

        for item in kospi_code_name_list:
            print(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = KiwoomAPI()
    test.login()
    myWindow = MyWindow()
    myWindow.show()
    time.sleep(5)
    test.btn1_clicked()
    sys.exit(app.exec_())
