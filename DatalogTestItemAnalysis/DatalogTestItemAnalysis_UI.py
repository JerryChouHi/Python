# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatalogTestItemAnalysis_UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(718, 458)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:/Users/zhoulei2/.designer/backup/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Open_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Open_lineEdit.setGeometry(QtCore.QRect(80, 230, 450, 30))
        self.Open_lineEdit.setReadOnly(True)
        self.Open_lineEdit.setObjectName("Open_lineEdit")
        self.Open_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Open_pushButton.setGeometry(QtCore.QRect(550, 230, 75, 30))
        self.Open_pushButton.setMouseTracking(False)
        self.Open_pushButton.setObjectName("Open_pushButton")
        self.Run_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Run_pushButton.setGeometry(QtCore.QRect(80, 350, 90, 30))
        self.Run_pushButton.setObjectName("Run_pushButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(80, 410, 541, 25))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.Sigma_label = QtWidgets.QLabel(self.centralwidget)
        self.Sigma_label.setGeometry(QtCore.QRect(80, 290, 91, 20))
        self.Sigma_label.setObjectName("Sigma_label")
        self.Sigma_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Sigma_lineEdit.setGeometry(QtCore.QRect(170, 290, 91, 20))
        self.Sigma_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Sigma_lineEdit.setObjectName("Sigma_lineEdit")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(80, 30, 550, 171))
        self.textBrowser.setObjectName("textBrowser")
        self.DPI_label = QtWidgets.QLabel(self.centralwidget)
        self.DPI_label.setGeometry(QtCore.QRect(350, 290, 91, 20))
        self.DPI_label.setObjectName("DPI_label")
        self.DPI_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.DPI_lineEdit.setGeometry(QtCore.QRect(440, 290, 91, 20))
        self.DPI_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.DPI_lineEdit.setObjectName("DPI_lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DatalogTestItemAnalysis"))
        self.Open_pushButton.setText(_translate("MainWindow", "Open"))
        self.Run_pushButton.setText(_translate("MainWindow", "Run"))
        self.Sigma_label.setText(_translate("MainWindow", "Sigma"))
        self.Sigma_lineEdit.setText(_translate("MainWindow", "3"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">1.点击Open，选择csv文件</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">2.输入数据：</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">  Sigma(采用数据的范围，默认值：3)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">  DPI(图像每英寸长度内的像素点数，默认值：300)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">3.点击Run</span></p></body></html>"))
        self.DPI_label.setText(_translate("MainWindow", "DPI"))
        self.DPI_lineEdit.setText(_translate("MainWindow", "300"))

