# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Datalog_Analysis_UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(752, 591)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icos/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(7.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(640, 480))
        self.groupBox.setMaximumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.groupBox.setFont(font)
        self.groupBox.setTitle("")
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.LoLimitRowNum_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.LoLimitRowNum_lineEdit.setObjectName("LoLimitRowNum_lineEdit")
        self.gridLayout.addWidget(self.LoLimitRowNum_lineEdit, 2, 3, 1, 1)
        self.LoLimitRowNum_label = QtWidgets.QLabel(self.groupBox)
        self.LoLimitRowNum_label.setObjectName("LoLimitRowNum_label")
        self.gridLayout.addWidget(self.LoLimitRowNum_label, 2, 2, 1, 1)
        self.TestDataRowNum_label = QtWidgets.QLabel(self.groupBox)
        self.TestDataRowNum_label.setObjectName("TestDataRowNum_label")
        self.gridLayout.addWidget(self.TestDataRowNum_label, 3, 0, 1, 1)
        self.TestDataColLetter_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.TestDataColLetter_lineEdit.setObjectName("TestDataColLetter_lineEdit")
        self.gridLayout.addWidget(self.TestDataColLetter_lineEdit, 3, 3, 1, 1)
        self.HiLimitRowNum_label = QtWidgets.QLabel(self.groupBox)
        self.HiLimitRowNum_label.setObjectName("HiLimitRowNum_label")
        self.gridLayout.addWidget(self.HiLimitRowNum_label, 2, 0, 1, 1)
        self.HiLimitRowNum_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.HiLimitRowNum_lineEdit.setObjectName("HiLimitRowNum_lineEdit")
        self.gridLayout.addWidget(self.HiLimitRowNum_lineEdit, 2, 1, 1, 1)
        self.EndColLetter = QtWidgets.QLabel(self.groupBox)
        self.EndColLetter.setObjectName("EndColLetter")
        self.gridLayout.addWidget(self.EndColLetter, 6, 2, 1, 1)
        self.TestDataColLetter_label = QtWidgets.QLabel(self.groupBox)
        self.TestDataColLetter_label.setObjectName("TestDataColLetter_label")
        self.gridLayout.addWidget(self.TestDataColLetter_label, 3, 2, 1, 1)
        self.OpenPath_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.OpenPath_lineEdit.setReadOnly(True)
        self.OpenPath_lineEdit.setObjectName("OpenPath_lineEdit")
        self.gridLayout.addWidget(self.OpenPath_lineEdit, 1, 0, 1, 3)
        self.TestDataRowNum_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.TestDataRowNum_lineEdit.setObjectName("TestDataRowNum_lineEdit")
        self.gridLayout.addWidget(self.TestDataRowNum_lineEdit, 3, 1, 1, 1)
        self.EndColLetter_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.EndColLetter_lineEdit.setObjectName("EndColLetter_lineEdit")
        self.gridLayout.addWidget(self.EndColLetter_lineEdit, 6, 3, 1, 1)
        self.Analysis_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.Analysis_pushButton.setObjectName("Analysis_pushButton")
        self.gridLayout.addWidget(self.Analysis_pushButton, 7, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 8, 0, 1, 4)
        self.BeginColLetter = QtWidgets.QLabel(self.groupBox)
        self.BeginColLetter.setObjectName("BeginColLetter")
        self.gridLayout.addWidget(self.BeginColLetter, 6, 0, 1, 1)
        self.Open_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.Open_pushButton.setMouseTracking(False)
        self.Open_pushButton.setObjectName("Open_pushButton")
        self.gridLayout.addWidget(self.Open_pushButton, 1, 3, 1, 1)
        self.BeginColLetter_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.BeginColLetter_lineEdit.setObjectName("BeginColLetter_lineEdit")
        self.gridLayout.addWidget(self.BeginColLetter_lineEdit, 6, 1, 1, 1)
        self.CostTime_label = QtWidgets.QLabel(self.groupBox)
        self.CostTime_label.setText("")
        self.CostTime_label.setObjectName("CostTime_label")
        self.gridLayout.addWidget(self.CostTime_label, 7, 3, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.SingleFile_radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.SingleFile_radioButton.setGeometry(QtCore.QRect(243, 20, 83, 16))
        self.SingleFile_radioButton.setObjectName("SingleFile_radioButton")
        self.DateFolder_radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.DateFolder_radioButton.setGeometry(QtCore.QRect(65, 20, 83, 16))
        self.DateFolder_radioButton.setObjectName("DateFolder_radioButton")
        self.LotFolder_radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.LotFolder_radioButton.setGeometry(QtCore.QRect(160, 20, 77, 16))
        self.LotFolder_radioButton.setObjectName("LotFolder_radioButton")
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 4)
        self.AllTestData_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.AllTestData_radioButton.setObjectName("AllTestData_radioButton")
        self.gridLayout.addWidget(self.AllTestData_radioButton, 5, 0, 1, 1)
        self.TestItemRowNum_label = QtWidgets.QLabel(self.groupBox)
        self.TestItemRowNum_label.setObjectName("TestItemRowNum_label")
        self.gridLayout.addWidget(self.TestItemRowNum_label, 4, 0, 1, 1)
        self.TestItemRowNum_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.TestItemRowNum_lineEdit.setObjectName("TestItemRowNum_lineEdit")
        self.gridLayout.addWidget(self.TestItemRowNum_lineEdit, 4, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Datalog Analysis"))
        self.LoLimitRowNum_label.setText(_translate("MainWindow", "LoLimitRowNum"))
        self.TestDataRowNum_label.setText(_translate("MainWindow", "TestDataRowNum"))
        self.HiLimitRowNum_label.setText(_translate("MainWindow", "HiLimitRowNum"))
        self.EndColLetter.setText(_translate("MainWindow", "EndColLetter"))
        self.TestDataColLetter_label.setText(_translate("MainWindow", "TestDataColLetter"))
        self.Analysis_pushButton.setText(_translate("MainWindow", "Analysis"))
        self.BeginColLetter.setText(_translate("MainWindow", "BeginColLetter"))
        self.Open_pushButton.setText(_translate("MainWindow", "Open"))
        self.SingleFile_radioButton.setText(_translate("MainWindow", "SingleFile"))
        self.DateFolder_radioButton.setText(_translate("MainWindow", "DateFolder"))
        self.LotFolder_radioButton.setText(_translate("MainWindow", "LotFolder"))
        self.AllTestData_radioButton.setText(_translate("MainWindow", "AllTestData"))
        self.TestItemRowNum_label.setText(_translate("MainWindow", "TestItemRowNum"))

