# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Datalog_Total_Analysis_UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icos/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ProjectFolder_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.ProjectFolder_radioButton.setGeometry(QtCore.QRect(50, 20, 100, 30))
        self.ProjectFolder_radioButton.setObjectName("ProjectFolder_radioButton")
        self.HandlerFolder_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.HandlerFolder_radioButton.setGeometry(QtCore.QRect(170, 20, 100, 30))
        self.HandlerFolder_radioButton.setObjectName("HandlerFolder_radioButton")
        self.Open_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Open_lineEdit.setGeometry(QtCore.QRect(50, 80, 500, 50))
        self.Open_lineEdit.setReadOnly(True)
        self.Open_lineEdit.setObjectName("Open_lineEdit")
        self.Open_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Open_pushButton.setGeometry(QtCore.QRect(580, 80, 170, 50))
        self.Open_pushButton.setObjectName("Open_pushButton")
        self.Project_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.Project_comboBox.setGeometry(QtCore.QRect(50, 180, 200, 50))
        self.Project_comboBox.setObjectName("Project_comboBox")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(50, 280, 700, 30))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.Analysis_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Analysis_pushButton.setGeometry(QtCore.QRect(280, 180, 170, 50))
        self.Analysis_pushButton.setObjectName("Analysis_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Datalog Total Analysis"))
        self.ProjectFolder_radioButton.setText(_translate("MainWindow", "ProjectFolder"))
        self.HandlerFolder_radioButton.setText(_translate("MainWindow", "HandlerFolder"))
        self.Open_pushButton.setText(_translate("MainWindow", "Open"))
        self.Analysis_pushButton.setText(_translate("MainWindow", "Analysis"))

