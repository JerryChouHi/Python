# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mathematics.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(434, 345)
        MainWindow.setMinimumSize(QtCore.QSize(400, 320))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_01 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_01.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_01.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_01.setReadOnly(True)
        self.lineEdit_01.setObjectName("lineEdit_01")
        self.gridLayout.addWidget(self.lineEdit_01, 0, 0, 1, 1)
        self.label_01 = QtWidgets.QLabel(self.groupBox)
        self.label_01.setMinimumSize(QtCore.QSize(30, 0))
        self.label_01.setText("")
        self.label_01.setAlignment(QtCore.Qt.AlignCenter)
        self.label_01.setObjectName("label_01")
        self.gridLayout.addWidget(self.label_01, 0, 1, 1, 1)
        self.lineEdit_02 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_02.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_02.setReadOnly(True)
        self.lineEdit_02.setObjectName("lineEdit_02")
        self.gridLayout.addWidget(self.lineEdit_02, 0, 2, 1, 1)
        self.label_02 = QtWidgets.QLabel(self.groupBox)
        self.label_02.setAlignment(QtCore.Qt.AlignCenter)
        self.label_02.setObjectName("label_02")
        self.gridLayout.addWidget(self.label_02, 0, 3, 1, 1)
        self.lineEdit_03 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_03.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_03.setObjectName("lineEdit_03")
        self.gridLayout.addWidget(self.lineEdit_03, 0, 4, 1, 1)
        self.lineEdit_04 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_04.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_04.setReadOnly(True)
        self.lineEdit_04.setObjectName("lineEdit_04")
        self.gridLayout.addWidget(self.lineEdit_04, 0, 5, 1, 1)
        self.label_03 = QtWidgets.QLabel(self.groupBox)
        self.label_03.setMinimumSize(QtCore.QSize(40, 0))
        self.label_03.setText("")
        self.label_03.setObjectName("label_03")
        self.gridLayout.addWidget(self.label_03, 0, 6, 1, 1)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_11.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_11.setReadOnly(True)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.gridLayout.addWidget(self.lineEdit_11, 1, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setMinimumSize(QtCore.QSize(30, 0))
        self.label_11.setText("")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 1, 1, 1, 1)
        self.lineEdit_12 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_12.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_12.setReadOnly(True)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.gridLayout.addWidget(self.lineEdit_12, 1, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 1, 3, 1, 1)
        self.lineEdit_13 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_13.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.gridLayout.addWidget(self.lineEdit_13, 1, 4, 1, 1)
        self.lineEdit_14 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_14.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_14.setReadOnly(True)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.gridLayout.addWidget(self.lineEdit_14, 1, 5, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setMinimumSize(QtCore.QSize(40, 0))
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 1, 6, 1, 1)
        self.lineEdit_21 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_21.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_21.setReadOnly(True)
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.gridLayout.addWidget(self.lineEdit_21, 2, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.groupBox)
        self.label_21.setMinimumSize(QtCore.QSize(30, 0))
        self.label_21.setText("")
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 2, 1, 1, 1)
        self.lineEdit_22 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_22.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_22.setReadOnly(True)
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.gridLayout.addWidget(self.lineEdit_22, 2, 2, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.groupBox)
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 2, 3, 1, 1)
        self.lineEdit_23 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_23.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.gridLayout.addWidget(self.lineEdit_23, 2, 4, 1, 1)
        self.lineEdit_24 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_24.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_24.setReadOnly(True)
        self.lineEdit_24.setObjectName("lineEdit_24")
        self.gridLayout.addWidget(self.lineEdit_24, 2, 5, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.groupBox)
        self.label_23.setMinimumSize(QtCore.QSize(40, 0))
        self.label_23.setText("")
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 2, 6, 1, 1)
        self.lineEdit_31 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_31.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_31.setReadOnly(True)
        self.lineEdit_31.setObjectName("lineEdit_31")
        self.gridLayout.addWidget(self.lineEdit_31, 3, 0, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.groupBox)
        self.label_31.setMinimumSize(QtCore.QSize(30, 0))
        self.label_31.setText("")
        self.label_31.setAlignment(QtCore.Qt.AlignCenter)
        self.label_31.setObjectName("label_31")
        self.gridLayout.addWidget(self.label_31, 3, 1, 1, 1)
        self.lineEdit_32 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_32.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_32.setReadOnly(True)
        self.lineEdit_32.setObjectName("lineEdit_32")
        self.gridLayout.addWidget(self.lineEdit_32, 3, 2, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.groupBox)
        self.label_32.setAlignment(QtCore.Qt.AlignCenter)
        self.label_32.setObjectName("label_32")
        self.gridLayout.addWidget(self.label_32, 3, 3, 1, 1)
        self.lineEdit_33 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_33.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_33.setObjectName("lineEdit_33")
        self.gridLayout.addWidget(self.lineEdit_33, 3, 4, 1, 1)
        self.lineEdit_34 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_34.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_34.setReadOnly(True)
        self.lineEdit_34.setObjectName("lineEdit_34")
        self.gridLayout.addWidget(self.lineEdit_34, 3, 5, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.groupBox)
        self.label_33.setMinimumSize(QtCore.QSize(40, 0))
        self.label_33.setText("")
        self.label_33.setObjectName("label_33")
        self.gridLayout.addWidget(self.label_33, 3, 6, 1, 1)
        self.lineEdit_41 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_41.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_41.setReadOnly(True)
        self.lineEdit_41.setObjectName("lineEdit_41")
        self.gridLayout.addWidget(self.lineEdit_41, 4, 0, 1, 1)
        self.label_41 = QtWidgets.QLabel(self.groupBox)
        self.label_41.setMinimumSize(QtCore.QSize(30, 0))
        self.label_41.setText("")
        self.label_41.setAlignment(QtCore.Qt.AlignCenter)
        self.label_41.setObjectName("label_41")
        self.gridLayout.addWidget(self.label_41, 4, 1, 1, 1)
        self.lineEdit_42 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_42.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_42.setReadOnly(True)
        self.lineEdit_42.setObjectName("lineEdit_42")
        self.gridLayout.addWidget(self.lineEdit_42, 4, 2, 1, 1)
        self.label_42 = QtWidgets.QLabel(self.groupBox)
        self.label_42.setAlignment(QtCore.Qt.AlignCenter)
        self.label_42.setObjectName("label_42")
        self.gridLayout.addWidget(self.label_42, 4, 3, 1, 1)
        self.lineEdit_43 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_43.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_43.setObjectName("lineEdit_43")
        self.gridLayout.addWidget(self.lineEdit_43, 4, 4, 1, 1)
        self.lineEdit_44 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_44.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_44.setReadOnly(True)
        self.lineEdit_44.setObjectName("lineEdit_44")
        self.gridLayout.addWidget(self.lineEdit_44, 4, 5, 1, 1)
        self.label_43 = QtWidgets.QLabel(self.groupBox)
        self.label_43.setMinimumSize(QtCore.QSize(40, 0))
        self.label_43.setText("")
        self.label_43.setObjectName("label_43")
        self.gridLayout.addWidget(self.label_43, 4, 6, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_refresh = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_refresh.setObjectName("pushButton_refresh")
        self.gridLayout_2.addWidget(self.pushButton_refresh, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.lineEdit_goal = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_goal.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_goal.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_goal.setReadOnly(True)
        self.lineEdit_goal.setObjectName("lineEdit_goal")
        self.gridLayout_2.addWidget(self.lineEdit_goal, 0, 6, 1, 1)
        self.label_goal = QtWidgets.QLabel(self.groupBox_2)
        self.label_goal.setObjectName("label_goal")
        self.gridLayout_2.addWidget(self.label_goal, 0, 5, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(246, 21, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 0, 1, 5)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 2, 1, 1)
        self.pushButton_check = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_check.setObjectName("pushButton_check")
        self.gridLayout_2.addWidget(self.pushButton_check, 1, 4, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 5, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox_2, 2, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "小学算术"))
        self.label_02.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">=</span></p></body></html>"))
        self.label_12.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">=</span></p></body></html>"))
        self.label_22.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">=</span></p></body></html>"))
        self.label_32.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">=</span></p></body></html>"))
        self.label_42.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">=</span></p></body></html>"))
        self.pushButton_refresh.setText(_translate("MainWindow", "刷新"))
        self.label_goal.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">得分</span></p></body></html>"))
        self.pushButton_check.setText(_translate("MainWindow", "检查√×"))

