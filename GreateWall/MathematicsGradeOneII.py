# encoding:utf-8
# @Time     : 2020/3/26 13:55
# @Author   : Jerry Chou
# @File     : PrimarySchoolMathematics.py
# @Function :

from sys import argv, exit
import Mathematics
import ChooseTopicTypeGradeOneII
import money
from PyQt5.QtWidgets import QApplication, QMainWindow
from random import randint


class moneyMainWindow(QMainWindow, money.Ui_MainWindow):
    def __init__(self):
        super(moneyMainWindow, self).__init__()
        self.setupUi(self)
        self.Refresh()
        self.pushButton_check.clicked.connect(self.Check)
        self.pushButton_refresh.clicked.connect(self.Refresh)

    def Refresh(self):
        self.lineEdit_03.setText('')
        self.lineEdit_04.setText('')
        self.label_05.setText('')

        self.lineEdit_12.setText('')
        self.lineEdit_13.setText('')
        self.lineEdit_14.setText('')
        self.label_15.setText('')

        self.lineEdit_23.setText('')
        self.lineEdit_24.setText('')
        self.label_25.setText('')

        self.lineEdit_32.setText('')
        self.lineEdit_33.setText('')
        self.lineEdit_34.setText('')
        self.label_35.setText('')

        self.lineEdit_43.setText('')
        self.lineEdit_44.setText('')
        self.label_46.setText('')

        self.lineEdit_01.setText(str(randint(1, 9)))
        self.lineEdit_02.setText(str(randint(1, 9)))

        self.lineEdit_11.setText(str(randint(11, 99)))

        self.lineEdit_21.setText(str(randint(1, 9)))
        self.lineEdit_22.setText(str(randint(1, 9)))

        self.lineEdit_31.setText(str(randint(11, 99)))

        self.lineEdit_41.setText(str(randint(1, 9)))
        self.lineEdit_42.setText(str(randint(1, 9)))

    def Check(self):
        rightCount = 0
        self.lineEdit_04.setText(self.lineEdit_01.text() + self.lineEdit_02.text())
        self.lineEdit_14.setText(self.lineEdit_11.text()[0] + ',' + self.lineEdit_11.text()[1])
        self.lineEdit_24.setText(self.lineEdit_21.text() + self.lineEdit_22.text())
        self.lineEdit_34.setText(self.lineEdit_31.text()[0] + ',' + self.lineEdit_31.text()[1])
        self.lineEdit_44.setText(str(10 * int(self.lineEdit_41.text()) - int(self.lineEdit_42.text())))
        if self.lineEdit_03.text() == self.lineEdit_04.text():
            self.label_05.setText('√')
            self.label_05.setStyleSheet('color:green')
            rightCount += 1
        else:
            self.label_05.setText('×')
            self.label_05.setStyleSheet('color:red')
        if self.lineEdit_12.text() == self.lineEdit_14.text()[0] and self.lineEdit_13.text() == \
                self.lineEdit_14.text()[-1]:
            self.label_15.setText('√')
            self.label_15.setStyleSheet('color:green')
            rightCount += 1
        else:
            self.label_15.setText('×')
            self.label_15.setStyleSheet('color:red')
        if self.lineEdit_23.text() == self.lineEdit_24.text():
            self.label_25.setText('√')
            self.label_25.setStyleSheet('color:green')
            rightCount += 1
        else:
            self.label_25.setText('×')
            self.label_25.setStyleSheet('color:red')
        if self.lineEdit_32.text() == self.lineEdit_34.text()[0] and self.lineEdit_33.text() == \
                self.lineEdit_34.text()[-1]:
            self.label_35.setText('√')
            self.label_35.setStyleSheet('color:green')
            rightCount += 1
        else:
            self.label_35.setText('×')
            self.label_35.setStyleSheet('color:red')
        if self.lineEdit_43.text() == self.lineEdit_44.text():
            self.label_46.setText('√')
            self.label_46.setStyleSheet('color:green')
            rightCount += 1
        else:
            self.label_46.setText('×')
            self.label_46.setStyleSheet('color:red')
        if rightCount < 3:
            self.lineEdit_goal.setStyleSheet('color:red')
        else:
            self.lineEdit_goal.setStyleSheet('color:green')
        self.lineEdit_goal.setText(str(rightCount * 20))


class GradeOneIIMainWindow(QMainWindow, Mathematics.Ui_MainWindow):
    def __init__(self, limit, symbol, mode):
        super(GradeOneIIMainWindow, self).__init__()
        self.limit = int(limit)
        self.symbol = symbol
        self.mode = mode
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
        if self.symbol == '+' and self.mode == 'hard':
            while True:
                randNum = randint(1, self.limit - 11)
                if randNum % 10 != 0:
                    break
        elif self.symbol == '-' and self.mode == 'hard':
            while True:
                randNum = randint(10, self.limit)
                if str(randNum)[-1] != '9':
                    break
        else:
            randNum = randint(1, self.limit - 1)
        return str(randNum)

    def GetSecondNum(self, firstNum):
        secondNum = 0
        if self.mode == 'easy':
            if self.symbol == '+':
                if len(firstNum) == 1:
                    secondNum += (10 * randint(0, 9) + randint(0, 9 - int(firstNum)))
                elif len(firstNum) == 2:
                    secondNum += (10 * randint(0, 9 - int(firstNum[0])) + randint(0, 9 - int(firstNum[1])))
            elif self.symbol == '-':
                if len(firstNum) == 1:
                    secondNum += (randint(0, int(firstNum)))
                elif len(firstNum) == 2:
                    secondNum += (10 * randint(0, int(firstNum[0])) + randint(0, int(firstNum[1])))
        elif self.mode == 'hard':
            if self.symbol == '+':
                if len(firstNum) == 1:
                    secondNum += (randint(10 - int(firstNum), 9))
                elif len(firstNum) == 2:
                    secondNum += (10 * randint(0, 8 - int(firstNum[0])) + randint(10 - int(firstNum[1]), 9))
            elif self.symbol == '-':
                secondNum += (10 * randint(0, int(firstNum[0]) - 1) + randint(int(firstNum[1]) + 1, 9))
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
                self.label_03.setText('√')
                self.label_03.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_03.setText('×')
                self.label_03.setStyleSheet('color:red')

            if self.lineEdit_13.text() == self.lineEdit_14.text():
                self.label_13.setText('√')
                self.label_13.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_13.setText('×')
                self.label_13.setStyleSheet('color:red')

            if self.lineEdit_23.text() == self.lineEdit_24.text():
                self.label_23.setText('√')
                self.label_23.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_23.setText('×')
                self.label_23.setStyleSheet('color:red')

            if self.lineEdit_33.text() == self.lineEdit_34.text():
                self.label_33.setText('√')
                self.label_33.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_33.setText('×')
                self.label_33.setStyleSheet('color:red')

            if self.lineEdit_43.text() == self.lineEdit_44.text():
                self.label_43.setText('√')
                self.label_43.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_43.setText('×')
                self.label_43.setStyleSheet('color:red')
        elif self.symbol == '-':
            self.lineEdit_04.setText(str(int(self.lineEdit_01.text()) - int(self.lineEdit_02.text())))
            self.lineEdit_14.setText(str(int(self.lineEdit_11.text()) - int(self.lineEdit_12.text())))
            self.lineEdit_24.setText(str(int(self.lineEdit_21.text()) - int(self.lineEdit_22.text())))
            self.lineEdit_34.setText(str(int(self.lineEdit_31.text()) - int(self.lineEdit_32.text())))
            self.lineEdit_44.setText(str(int(self.lineEdit_41.text()) - int(self.lineEdit_42.text())))

            if self.lineEdit_03.text() == self.lineEdit_04.text():
                self.label_03.setText('√')
                self.label_03.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_03.setText('×')
                self.label_03.setStyleSheet('color:red')

            if self.lineEdit_13.text() == self.lineEdit_14.text():
                self.label_13.setText('√')
                self.label_13.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_13.setText('×')
                self.label_13.setStyleSheet('color:red')

            if self.lineEdit_23.text() == self.lineEdit_24.text():
                self.label_23.setText('√')
                self.label_23.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_23.setText('×')
                self.label_23.setStyleSheet('color:red')

            if self.lineEdit_33.text() == self.lineEdit_34.text():
                self.label_33.setText('√')
                self.label_33.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_33.setText('×')
                self.label_33.setStyleSheet('color:red')

            if self.lineEdit_43.text() == self.lineEdit_44.text():
                self.label_43.setText('√')
                self.label_43.setStyleSheet('color:green')
                rightCount += 1
            else:
                self.label_43.setText('×')
                self.label_43.setStyleSheet('color:red')
        if rightCount < 3:
            self.lineEdit_goal.setStyleSheet('color:red')
        else:
            self.lineEdit_goal.setStyleSheet('color:green')
        self.lineEdit_goal.setText(str(rightCount * 20))


class ChooseWindow(QMainWindow, ChooseTopicTypeGradeOneII.Ui_MainWindow):
    def __init__(self):
        super(ChooseWindow, self).__init__()
        self.setupUi(self)

        self.pushButton_20_sub_hard.clicked.connect(lambda: self.ClickGoto(self.pushButton_20_sub_hard))
        self.pushButton_money.clicked.connect(lambda: self.ClickGoto(self.pushButton_money))
        self.pushButton_100_plus_easy.clicked.connect(lambda: self.ClickGoto(self.pushButton_100_plus_easy))
        self.pushButton_100_sub_easy.clicked.connect(lambda: self.ClickGoto(self.pushButton_100_sub_easy))
        self.pushButton_100_plus_hard.clicked.connect(lambda: self.ClickGoto(self.pushButton_100_plus_hard))
        self.pushButton_100_sub_hard.clicked.connect(lambda: self.ClickGoto(self.pushButton_100_sub_hard))

    def ClickGoto(self, button):
        buttonName = button.objectName()
        if buttonName != 'pushButton_money':
            buttonNameSplit = buttonName.split('_')
            limit = buttonNameSplit[1]
            if buttonNameSplit[2] == 'plus':
                symbol = '+'
            elif buttonNameSplit[2] == 'sub':
                symbol = '-'
            mode = buttonNameSplit[3]
            self.gotoUI = GradeOneIIMainWindow(limit, symbol, mode)
            self.gotoUI.setWindowTitle(button.text())
        else:
            self.gotoUI = moneyMainWindow()
            self.gotoUI.setWindowTitle(button.text())
        self.gotoUI.show()


if __name__ == '__main__':
    app = QApplication(argv)
    myChooseWindow = ChooseWindow()
    myChooseWindow.show()
    exit(app.exec_())
