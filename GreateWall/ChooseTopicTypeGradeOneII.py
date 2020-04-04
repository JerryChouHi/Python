# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChooseTopicTypeGradeOneII.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 270)
        MainWindow.setMinimumSize(QtCore.QSize(520, 270))
        MainWindow.setMaximumSize(QtCore.QSize(520, 270))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 500, 250))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_100_sub_easy = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_100_sub_easy.setObjectName("pushButton_100_sub_easy")
        self.gridLayout.addWidget(self.pushButton_100_sub_easy, 3, 1, 1, 1)
        self.pushButton_20_sub_hard = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_20_sub_hard.setObjectName("pushButton_20_sub_hard")
        self.gridLayout.addWidget(self.pushButton_20_sub_hard, 0, 0, 1, 1)
        self.pushButton_100_plus_easy = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_100_plus_easy.setObjectName("pushButton_100_plus_easy")
        self.gridLayout.addWidget(self.pushButton_100_plus_easy, 3, 0, 1, 1)
        self.pushButton_money = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_money.setObjectName("pushButton_money")
        self.gridLayout.addWidget(self.pushButton_money, 0, 1, 1, 1)
        self.pushButton_100_plus_hard = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_100_plus_hard.setObjectName("pushButton_100_plus_hard")
        self.gridLayout.addWidget(self.pushButton_100_plus_hard, 4, 0, 1, 1)
        self.pushButton_100_sub_hard = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_100_sub_hard.setObjectName("pushButton_100_sub_hard")
        self.gridLayout.addWidget(self.pushButton_100_sub_hard, 4, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "选择题目类型"))
        self.pushButton_100_sub_easy.setText(_translate("MainWindow", "100以内的减法（不退位）"))
        self.pushButton_20_sub_hard.setText(_translate("MainWindow", "20以内的退位减法"))
        self.pushButton_100_plus_easy.setText(_translate("MainWindow", "100以内的加法（不进位）"))
        self.pushButton_money.setText(_translate("MainWindow", "元、角、分"))
        self.pushButton_100_plus_hard.setText(_translate("MainWindow", "100以内的加法（进位）"))
        self.pushButton_100_sub_hard.setText(_translate("MainWindow", "100以内的减法（退位）"))

