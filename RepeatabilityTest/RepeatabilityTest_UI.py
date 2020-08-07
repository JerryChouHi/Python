# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RepeatabilityTest_UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(680, 539)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Datalog/icos/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.SingleFile_radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.SingleFile_radioButton.setGeometry(QtCore.QRect(210, 20, 100, 20))
        self.SingleFile_radioButton.setObjectName("SingleFile_radioButton")
        self.SourceFolder_radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.SourceFolder_radioButton.setGeometry(QtCore.QRect(90, 20, 100, 20))
        self.SourceFolder_radioButton.setObjectName("SourceFolder_radioButton")
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 3)
        self.Analysis_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.Analysis_pushButton.setObjectName("Analysis_pushButton")
        self.gridLayout.addWidget(self.Analysis_pushButton, 3, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 4, 0, 1, 3)
        self.OpenPath_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.OpenPath_lineEdit.setReadOnly(True)
        self.OpenPath_lineEdit.setObjectName("OpenPath_lineEdit")
        self.gridLayout.addWidget(self.OpenPath_lineEdit, 1, 0, 1, 2)
        self.Open_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.Open_pushButton.setMouseTracking(False)
        self.Open_pushButton.setObjectName("Open_pushButton")
        self.gridLayout.addWidget(self.Open_pushButton, 1, 2, 1, 1)
        self.DeleteDuplicate_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.DeleteDuplicate_radioButton.setObjectName("DeleteDuplicate_radioButton")
        self.gridLayout.addWidget(self.DeleteDuplicate_radioButton, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Repeatability Test"))
        self.SingleFile_radioButton.setText(_translate("MainWindow", "SingleFile"))
        self.SourceFolder_radioButton.setText(_translate("MainWindow", "SourceFolder"))
        self.Analysis_pushButton.setText(_translate("MainWindow", "Analysis"))
        self.Open_pushButton.setText(_translate("MainWindow", "Open"))
        self.DeleteDuplicate_radioButton.setText(_translate("MainWindow", "Delete continuous duplicate data"))

