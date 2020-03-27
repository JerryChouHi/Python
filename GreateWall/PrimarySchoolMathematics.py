# encoding:utf-8
# @Time     : 2020/3/26 13:55
# @Author   : Jerry Chou
# @File     : PrimarySchoolMathematics.py
# @Function :

from sys import argv, exit
from Mathematics import Ui_MainWindow
from ChooseTopicType import Ui_ChooseWindow
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow
from random import randint


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, s):
        super(MainWindow, self).__init__()
        self.s1 = s[0]
        self.s2 = s[1]
        self.setupUi(self)
        self.label_01.setFont(QFont('Timers', 20))
        self.label_11.setFont(QFont('Timers', 20))
        self.label_21.setFont(QFont('Timers', 20))
        self.label_31.setFont(QFont('Timers', 20))
        self.label_41.setFont(QFont('Timers', 20))
        self.refresh()
        self.pushButton_check.clicked.connect(self.check)
        self.pushButton_refresh.clicked.connect(self.refresh)

    def refresh(self):
        if self.s2 == '+':
            self.label_01.setText('+')
            self.label_11.setText('+')
            self.label_21.setText('+')
            self.label_31.setText('+')
            self.label_41.setText('+')
            if self.s1 == '1':
                self.lineEdit_01.setText(str(randint(0, 9)))
                self.lineEdit_11.setText(str(randint(0, 9)))
                self.lineEdit_21.setText(str(randint(0, 9)))
                self.lineEdit_31.setText(str(randint(0, 9)))
                self.lineEdit_41.setText(str(randint(0, 9)))

                self.lineEdit_02.setText(str(randint(0, 9)))
                self.lineEdit_12.setText(str(randint(0, 9)))
                self.lineEdit_22.setText(str(randint(0, 9)))
                self.lineEdit_32.setText(str(randint(0, 9)))
                self.lineEdit_42.setText(str(randint(0, 9)))
            elif self.s1 == '2':
                self.lineEdit_01.setText(str(randint(0, 99)))
                self.lineEdit_11.setText(str(randint(0, 99)))
                self.lineEdit_21.setText(str(randint(0, 99)))
                self.lineEdit_31.setText(str(randint(0, 99)))
                self.lineEdit_41.setText(str(randint(0, 99)))

                self.lineEdit_02.setText(str(randint(0, 99)))
                self.lineEdit_12.setText(str(randint(0, 99)))
                self.lineEdit_22.setText(str(randint(0, 99)))
                self.lineEdit_32.setText(str(randint(0, 99)))
                self.lineEdit_42.setText(str(randint(0, 99)))
        elif self.s2 == '-':
            self.label_01.setText('-')
            self.label_11.setText('-')
            self.label_21.setText('-')
            self.label_31.setText('-')
            self.label_41.setText('-')
            if self.s1 == '1':
                self.lineEdit_01.setText(str(randint(0, 9)))
                self.lineEdit_11.setText(str(randint(0, 9)))
                self.lineEdit_21.setText(str(randint(0, 9)))
                self.lineEdit_31.setText(str(randint(0, 9)))
                self.lineEdit_41.setText(str(randint(0, 9)))

                self.lineEdit_02.setText(str(randint(0, int(self.lineEdit_01.text()))))
                self.lineEdit_12.setText(str(randint(0, int(self.lineEdit_11.text()))))
                self.lineEdit_22.setText(str(randint(0, int(self.lineEdit_21.text()))))
                self.lineEdit_32.setText(str(randint(0, int(self.lineEdit_31.text()))))
                self.lineEdit_42.setText(str(randint(0, int(self.lineEdit_41.text()))))
            elif self.s1 == '2':
                self.lineEdit_01.setText(str(randint(10, 99)))
                self.lineEdit_11.setText(str(randint(10, 99)))
                self.lineEdit_21.setText(str(randint(10, 99)))
                self.lineEdit_31.setText(str(randint(10, 99)))
                self.lineEdit_41.setText(str(randint(10, 99)))

                self.lineEdit_02.setText(str(randint(10, int(self.lineEdit_01.text()))))
                self.lineEdit_12.setText(str(randint(10, int(self.lineEdit_11.text()))))
                self.lineEdit_22.setText(str(randint(10, int(self.lineEdit_21.text()))))
                self.lineEdit_32.setText(str(randint(10, int(self.lineEdit_31.text()))))
                self.lineEdit_42.setText(str(randint(10, int(self.lineEdit_41.text()))))

    def check(self):
        rightCount = 0
        if self.s2 == '+':
            self.lineEdit_04.setText(str(int(self.lineEdit_01.text()) + int(self.lineEdit_02.text())))
            self.lineEdit_14.setText(str(int(self.lineEdit_11.text()) + int(self.lineEdit_12.text())))
            self.lineEdit_24.setText(str(int(self.lineEdit_21.text()) + int(self.lineEdit_22.text())))
            self.lineEdit_34.setText(str(int(self.lineEdit_31.text()) + int(self.lineEdit_32.text())))
            self.lineEdit_44.setText(str(int(self.lineEdit_41.text()) + int(self.lineEdit_42.text())))

            if self.lineEdit_03.text() == self.lineEdit_04.text():
                self.label_03.setText('答对')
                self.label_03.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_03.setText('答错')
                self.label_03.setStyleSheet('color:red')

            if self.lineEdit_13.text() == self.lineEdit_14.text():
                self.label_13.setText('答对')
                self.label_13.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_13.setText('答错')
                self.label_13.setStyleSheet('color:red')

            if self.lineEdit_23.text() == self.lineEdit_24.text():
                self.label_23.setText('答对')
                self.label_23.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_23.setText('答错')
                self.label_23.setStyleSheet('color:red')

            if self.lineEdit_33.text() == self.lineEdit_34.text():
                self.label_33.setText('答对')
                self.label_33.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_33.setText('答错')
                self.label_33.setStyleSheet('color:red')

            if self.lineEdit_43.text() == self.lineEdit_44.text():
                self.label_43.setText('答对')
                self.label_43.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_43.setText('答错')
                self.label_43.setStyleSheet('color:red')
        elif self.s2 == '-':
            self.lineEdit_04.setText(str(int(self.lineEdit_01.text()) - int(self.lineEdit_02.text())))
            self.lineEdit_14.setText(str(int(self.lineEdit_11.text()) - int(self.lineEdit_12.text())))
            self.lineEdit_24.setText(str(int(self.lineEdit_21.text()) - int(self.lineEdit_22.text())))
            self.lineEdit_34.setText(str(int(self.lineEdit_31.text()) - int(self.lineEdit_32.text())))
            self.lineEdit_44.setText(str(int(self.lineEdit_41.text()) - int(self.lineEdit_42.text())))

            if self.lineEdit_03.text() == self.lineEdit_04.text():
                self.label_03.setText('答对')
                self.label_03.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_03.setText('答错')
                self.label_03.setStyleSheet('color:red')

            if self.lineEdit_13.text() == self.lineEdit_14.text():
                self.label_13.setText('答对')
                self.label_13.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_13.setText('答错')
                self.label_13.setStyleSheet('color:red')

            if self.lineEdit_23.text() == self.lineEdit_24.text():
                self.label_23.setText('答对')
                self.label_23.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_23.setText('答错')
                self.label_23.setStyleSheet('color:red')

            if self.lineEdit_33.text() == self.lineEdit_34.text():
                self.label_33.setText('答对')
                self.label_33.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_33.setText('答错')
                self.label_33.setStyleSheet('color:red')

            if self.lineEdit_43.text() == self.lineEdit_44.text():
                self.label_43.setText('答对')
                self.label_43.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_43.setText('答错')
                self.label_43.setStyleSheet('color:red')
        if rightCount < 3:
            self.lineEdit_goal.setStyleSheet('color:red')
        else:
            self.lineEdit_goal.setStyleSheet('color:green')
        self.lineEdit_goal.setText(str(rightCount * 20))


class ChooseWindow(QMainWindow, Ui_ChooseWindow):
    def __init__(self):
        super(ChooseWindow, self).__init__()
        self.setupUi(self)

        self.pushButton_1plus.clicked.connect(lambda: self.re('1+'))
        self.pushButton_1sub.clicked.connect(lambda: self.re('1-'))
        self.pushButton_2plus.clicked.connect(lambda: self.re('2+'))
        self.pushButton_2sub.clicked.connect(lambda: self.re('2-'))

    def re(self, s):
        self.ui = MainWindow(s)
        self.ui.show()


if __name__ == '__main__':
    app = QApplication(argv)
    myChooseWindow = ChooseWindow()
    myChooseWindow.show()
    exit(app.exec_())
