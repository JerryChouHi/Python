# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OV_Image_Collation_UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.OpenPath_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.OpenPath_lineEdit.setGeometry(QtCore.QRect(100, 50, 451, 30))
        self.OpenPath_lineEdit.setReadOnly(True)
        self.OpenPath_lineEdit.setObjectName("OpenPath_lineEdit")
        self.Open_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Open_pushButton.setGeometry(QtCore.QRect(570, 50, 75, 30))
        self.Open_pushButton.setMouseTracking(False)
        self.Open_pushButton.setObjectName("Open_pushButton")
        self.GatherData_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.GatherData_pushButton.setGeometry(QtCore.QRect(100, 130, 90, 30))
        self.GatherData_pushButton.setObjectName("GatherData_pushButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(100, 200, 541, 25))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OV Image Collation"))
        self.Open_pushButton.setText(_translate("MainWindow", "Open"))
        self.GatherData_pushButton.setText(_translate("MainWindow", "Gather Data"))

