# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Word2HTML_UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 511)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.OpenPath_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.OpenPath_lineEdit.setGeometry(QtCore.QRect(90, 241, 420, 21))
        self.OpenPath_lineEdit.setReadOnly(True)
        self.OpenPath_lineEdit.setObjectName("OpenPath_lineEdit")
        self.Convert_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Convert_pushButton.setGeometry(QtCore.QRect(90, 302, 101, 23))
        self.Convert_pushButton.setObjectName("Convert_pushButton")
        self.Open_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Open_pushButton.setGeometry(QtCore.QRect(530, 240, 180, 23))
        self.Open_pushButton.setMouseTracking(False)
        self.Open_pushButton.setObjectName("Open_pushButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(90, 370, 620, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.CostTime_label = QtWidgets.QLabel(self.centralwidget)
        self.CostTime_label.setGeometry(QtCore.QRect(540, 430, 171, 21))
        self.CostTime_label.setText("")
        self.CostTime_label.setObjectName("CostTime_label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(90, 30, 621, 161))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Word2HTML"))
        self.Convert_pushButton.setText(_translate("MainWindow", "Convert"))
        self.Open_pushButton.setText(_translate("MainWindow", "Open"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">操作步骤：</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">1.打开.docx文件所在文件夹</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">2.点击Convert</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">转换结果：</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">一个.docx文件对应生成一个.html文件</span></p></body></html>"))

