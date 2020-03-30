# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChooseTopicType.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 200)
        MainWindow.setMinimumSize(QtCore.QSize(320, 200))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 301, 171))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_1plus = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_1plus.setObjectName("pushButton_1plus")
        self.gridLayout.addWidget(self.pushButton_1plus, 0, 0, 1, 1)
        self.pushButton_1sub = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_1sub.setObjectName("pushButton_1sub")
        self.gridLayout.addWidget(self.pushButton_1sub, 0, 1, 1, 1)
        self.pushButton_2plus = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2plus.setObjectName("pushButton_2plus")
        self.gridLayout.addWidget(self.pushButton_2plus, 1, 0, 1, 1)
        self.pushButton_2sub = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2sub.setObjectName("pushButton_2sub")
        self.gridLayout.addWidget(self.pushButton_2sub, 1, 1, 1, 1)
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

