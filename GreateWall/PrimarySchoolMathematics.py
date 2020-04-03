# encoding:utf-8
# @Time     : 2020/3/26 13:55
# @Author   : Jerry Chou
# @File     : PrimarySchoolMathematics.py
# @Function :

from sys import argv, exit
import Mathematics
import ChooseTopicType
from PyQt5.QtWidgets import QApplication, QMainWindow
from random import randint


class MainWindow(QMainWindow, Mathematics.Ui_MainWindow):
    def __init__(self, s):
        super(MainWindow, self).__init__()
        self.length = int(s[0])
        self.symbol = s[1]
        self.mode = s[2]
        self.setupUi(self)
        self.Refresh()
        self.pushButton_check.clicked.connect(self.Check)
        self.pushButton_refresh.clicked.connect(self.Refresh)

    def Refresh(self):
        self.lineEdit_03.setText('')
        self.lineEdit_04.setText('')
        self.label_03.setText('')

        self.lineEdit_13.setText('')
        self.lineEdit_14.setText('')
        self.label_13.setText('')

        self.lineEdit_23.setText('')
        self.lineEdit_24.setText('')
        self.label_23.setText('')

        self.lineEdit_33.setText('')
        self.lineEdit_34.setText('')
        self.label_33.setText('')

        self.lineEdit_43.setText('')
        self.lineEdit_44.setText('')
        self.label_43.setText('')

        self.lineEdit_01.setText(self.GetFirstNum())
        self.lineEdit_11.setText(self.GetFirstNum())
        self.lineEdit_21.setText(self.GetFirstNum())
        self.lineEdit_31.setText(self.GetFirstNum())
        self.lineEdit_41.setText(self.GetFirstNum())

        self.label_01.setText(self.symbol)
        self.label_11.setText(self.symbol)
        self.label_21.setText(self.symbol)
        self.label_31.setText(self.symbol)
        self.label_41.setText(self.symbol)

        self.lineEdit_02.setText(self.GetSecondNum(self.lineEdit_01.text()))
        self.lineEdit_12.setText(self.GetSecondNum(self.lineEdit_11.text()))
        self.lineEdit_22.setText(self.GetSecondNum(self.lineEdit_21.text()))
        self.lineEdit_32.setText(self.GetSecondNum(self.lineEdit_31.text()))
        self.lineEdit_42.setText(self.GetSecondNum(self.lineEdit_41.text()))

    def GetFirstNum(self):
        return str(randint(10 ** (self.length - 1), 10 ** self.length - 1))

    def GetSecondNum(self, firstNum):
        secondNum = 0
        if self.mode == 'E':
            for i in range(self.length):
                if self.symbol == '+':
                    secondNum += (10 ** (self.length - 1 - i) * randint(0, 9 - int(firstNum[i])))
                elif self.symbol == '-':
                    secondNum += (10 ** (self.length - 1 - i) * randint(0, int(firstNum[i])))
        elif self.mode == 'A':
            if self.symbol == '+':
                secondNum = randint(10 ** (self.length - 1), 10 ** self.length - 1)
            elif self.symbol == '-':
                secondNum = randint(10 ** (self.length - 1), int(firstNum))
        return str(secondNum)

    def Check(self):
        rightCount = 0
        if self.symbol == '+':
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
        elif self.symbol == '-':
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


class ChooseWindow(QMainWindow, ChooseTopicType.Ui_MainWindow):
    def __init__(self):
        super(ChooseWindow, self).__init__()
        self.setupUi(self)

        self.pushButton_1plus.clicked.connect(lambda: self.re('1+A', self.pushButton_1plus.text()))
        self.pushButton_1sub.clicked.connect(lambda: self.re('1-A', self.pushButton_1sub.text()))
        self.pushButton_2plus.clicked.connect(lambda: self.re('2+A', self.pushButton_2plus.text()))
        self.pushButton_2sub.clicked.connect(lambda: self.re('2-A', self.pushButton_2sub.text()))
        self.pushButton_2plusEasy.clicked.connect(lambda: self.re('2+E', self.pushButton_2plusEasy.text()))
        self.pushButton_2subEasy.clicked.connect(lambda: self.re('2-E', self.pushButton_2subEasy.text()))

    def re(self, s, title):
        self.ui = MainWindow(s)
        self.ui.setWindowTitle(title)
        self.ui.show()


if __name__ == '__main__':
    app = QApplication(argv)
    myChooseWindow = ChooseWindow()
    myChooseWindow.show()
    exit(app.exec_())
