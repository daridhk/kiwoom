# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tableWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1187, 277)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(40, 90, 1131, 121))
        self.tableWidget.setSizeIncrement(QtCore.QSize(1, 1))
        self.tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 20, 121, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(840, 30, 56, 20))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(900, 30, 141, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.btnStart = QtWidgets.QPushButton(Dialog)
        self.btnStart.setGeometry(QtCore.QRect(570, 230, 121, 41))
        self.btnStart.setObjectName("btnStart")
        self.btnClose = QtWidgets.QPushButton(Dialog)
        self.btnClose.setGeometry(QtCore.QRect(1030, 230, 111, 41))
        self.btnClose.setObjectName("btnClose")
        self.btnStop = QtWidgets.QPushButton(Dialog)
        self.btnStop.setGeometry(QtCore.QRect(710, 230, 121, 41))
        self.btnStop.setObjectName("btnStop")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "My title"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "item"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "expected pri"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "차수"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "budg"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "one pr"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "market"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "prof"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "target"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Dialog", "y/n"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Dialog", "period"))
        self.label.setText(_translate("Dialog", "auto"))
        self.label_2.setText(_translate("Dialog", "serial"))
        self.btnStart.setText(_translate("Dialog", "Start"))
        self.btnClose.setText(_translate("Dialog", "Close"))
        self.btnStop.setText(_translate("Dialog", "Stop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
