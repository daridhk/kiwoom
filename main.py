import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QCoreApplication, QDateTime, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import uic
import pandas as pd
from KiwoomAPI import *

from Worker import Worker
from tableWidget import *

class KiwoomAPIWindow(QMainWindow):
    def __init__(self, connect=1):
        super().__init__()
        self.title = 'AutoTrader'
        self.left = 50
        self.top = 50
        self.width = 640
        self.height = 480
        # self.initUI()
        self.connectKiwoom(connect)

    def connectKiwoom(self, connect=1):
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        if connect == 1:
            # API 연결
            self.kiwoom.dynamicCall("CommConnect()")

        # API 연결 되었는지를 Status Bar에 출력
        #self.kiwoom.OnEventConnect.connect(self.login_event)


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        # 라벨 생성
        label_market = QLabel('장 선택 ', self)
        label_market.move(10, 70)

        # 콤보 박스 생성
        self.cbox_market = QComboBox(self)
        self.cbox_market.setGeometry(100, 70, 150, 32)
        self.cbox_market.setObjectName(("box"))
        self.cbox_market.addItem("장내", userData=0)
        self.cbox_market.addItem("코스닥", userData=10)
        self.cbox_market.addItem("코넥스", userData=50)

        # 버튼 생성
        btn_market = QPushButton('장 리스트 가져오기', self)
        btn_market.setToolTip('0: 장내, 10: 코스닥, 50: 코넥스 등등등 Spec 참조 ')
        btn_market.resize(200, 32)
        btn_market.move(300, 70)
        btn_market.clicked.connect(self.on_click_market)

        btn1 = QPushButton('Quit', self)
        btn1.move(10,100)
        QToolTip.setFont(QFont('SansSerif',14))
        btn1.setToolTip('If pressed, it will <b>Quit</b>')
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(QCoreApplication.instance().quit)

        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        date = QDateTime.currentDateTime()
        self.statusBar().showMessage(date.toString(Qt.DefaultLocaleLongDate))

        # tableWidget
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(4)

        self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(20):
            for j in range(4):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(i+j)))

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)
        #delete so far

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login_event(self, error):
        if error == 0:
            strs = '로그인 성공 Code : ' + str(error)
            self.statusBar().showMessage(strs)
        else:
            strs = '로그인 실패 Code : ' + str(error)
            self.statusBar().showMessage(strs)

    def on_click_market(self):
        print(self.cbox_market.currentText(), ' ',self.cbox_market.currentData())
        # GetCodeListByMarket 으로 종목코드 요청
        result = self.kiwoom.dynamicCall('GetCodeListByMarket(QString)', str(self.cbox_market.currentData()))
        code_list = result.split(';')
        data_list = []

        for code in code_list:
            name = self.kiwoom.dynamicCall('GetMasterCodeName(QString)', code)
            data_list.append([name, code])

        # 데이터 프레임으로 만들기
        df = pd.DataFrame(data_list, columns=['회사명', '종목코드'])
        print(df.head())

Form_class, Window_class = uic.loadUiType("tableWidget.ui")

class MyWindow2(Form_class, Window_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnStart.setEnabled(False)

class MyWindow(Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.btnStart.setEnabled(False)
        self.btnStart.clicked.connect(self.start_transaction)
        self.btnStop.clicked.connect(self.stop_transaction)
        self.btnClose.clicked.connect(QCoreApplication.instance().quit)
        self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        #self.chbox = QCheckBox()
        #self.tableWidget.setCellWidget(0,1, self.chbox)
        self.connectKiwoom()

    def start_transaction(self):
        print('start_transaction')
        self.worker = Worker(self)
        self.worker.start()

    def stop_transaction(self):
        self.worker.terminate()
        print('stop_transaction')

    def connectKiwoom(self):
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

    def get_market_code(self):
        # GetCodeListByMarket 으로 종목코드 요청
        #result = self.kiwoom.dynamicCall('GetCodeListByMarket(QString)', ['0'])
        result = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
        return result
        code_list = result.split(';')
        return code_list

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    #kiwoom = KiwoomAPI()
    #codes = kiwoom.get_market_code()
    codes = window.get_market_code()
    print(codes)
    app.exec_()
