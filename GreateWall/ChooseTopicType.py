# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChooseTopicType.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChooseWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 240)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_1plus = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1plus.setGeometry(QtCore.QRect(50, 50, 91, 31))
        self.pushButton_1plus.setObjectName("pushButton_1plus")
        self.pushButton_1sub = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1sub.setGeometry(QtCore.QRect(170, 50, 91, 31))
        self.pushButton_1sub.setObjectName("pushButton_1sub")
        self.pushButton_2plus = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2plus.setGeometry(QtCore.QRect(50, 110, 91, 31))
        self.pushButton_2plus.setObjectName("pushButton_2plus")
        self.pushButton_2sub = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2sub.setGeometry(QtCore.QRect(170, 110, 91, 31))
        self.pushButton_2sub.setObjectName("pushButton_2sub")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "选择题目类型"))
        self.pushButton_1plus.setText(_translate("MainWindow", "一位数加法"))
        self.pushButton_1sub.setText(_translate("MainWindow", "一位数减法"))
        self.pushButton_2plus.setText(_translate("MainWindow", "两位数加法"))
        self.pushButton_2sub.setText(_translate("MainWindow", "两位数减法"))

