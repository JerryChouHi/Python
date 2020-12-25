# encoding:utf-8
# @Time     : 2020/4/15 17:24
# @Author   : Jerry Chou
# @File     : Word2HTML.py
# @Function :

from win32com.client import Dispatch
import datetime
from os.path import isdir, join
from os import listdir, getcwd
import Word2HTML_UI
from sys import argv, exit
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QFileDialog


def GetFileList(folder, postfix=None):
    """
    find a list of files with a postfix
    """
    fullNameList = []
    if isdir(folder):
        files = listdir(folder)
        for filename in files:
            fullNameList.append(join(folder, filename))
        if postfix:
            targetFileList = []
            for fullname in fullNameList:
                if fullname.endswith(postfix.upper()) or fullname.endswith(postfix.lower()):
                    targetFileList.append(fullname)
            return targetFileList
        else:
            return fullNameList
    else:
        print("Error：Not a folder!")
        return False


def doc2html(word_file):
    w = Dispatch('Word.Application')
    try:
        doc = w.Documents.Open(word_file, ReadOnly=1)
        html_file = word_file.replace('docx', 'html')
        doc.SaveAs(html_file, 8)
        doc.Close()
        w.Quit()
        return True
    except:
        return False


class RunThread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self, openPath):
        super(RunThread, self).__init__()
        self.openPath = openPath

    def run(self):
        global currentFileCount, totalFileCount
        fileList = GetFileList(self.openPath, '.docx')

        for file in fileList:
            currentFileCount += 1
            if currentFileCount != totalFileCount:
                self._signal.emit(str(currentFileCount * 100 // totalFileCount))
            rc = doc2html(file)
            if rc:
                print('{0} 转换成功.\n'.format(file))
            else:
                print('{0} 转换失败.\n'.format(file))
        self._signal.emit(str(100))


class MainWindow(QMainWindow, Word2HTML_UI.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.cwd = getcwd()
        self.qe = QErrorMessage(self)
        self.Open_pushButton.clicked.connect(self.Open)
        self.Convert_pushButton.clicked.connect(self.Convert)

    def Open(self):
        dirChoose = QFileDialog.getExistingDirectory(self, 'Select Directory', self.cwd)
        if not dirChoose:
            return
        self.OpenPath_lineEdit.setText(dirChoose)

    def CallBackLog(self, msg):
        self.progressBar.setValue(int(msg))  # pass the thread's parameters to progressBar
        if msg == '100':
            self.Convert_pushButton.setEnabled(True)
            costTime = str(datetime.datetime.now() - startTime)[:10]
            self.CostTime_label.setText('CostTime : ' + costTime)

    def Convert(self):
        if not self.OpenPath_lineEdit.text():
            self.qe.showMessage('Path cannot be empty!')
            return
        else:
            global startTime
            startTime = datetime.datetime.now()
            global totalFileCount
            totalFileCount = 0
            fileList = GetFileList(self.OpenPath_lineEdit.text(), '.docx')
            if not fileList:
                return
            totalFileCount += len(fileList)
            global currentFileCount
            currentFileCount = 0
            # create thread
            self.Convert_pushButton.setEnabled(False)
            self.thread = RunThread(self.OpenPath_lineEdit.text())
            # connect signal
            self.thread._signal.connect(self.CallBackLog)
            self.thread.start()


if __name__ == '__main__':
    fileList = GetFileList('H:\zhoulei2\Word2HTML\EvtITE_UserManual3\\UT3\Test', '.docx')

    for file in fileList:
        rc = doc2html(file)
        if rc:
            print('{0} 转换成功.'.format(file))
        else:
            print('{0} 转换失败.'.format(file))
    # app = QApplication(argv)
    # myMainWindow = MainWindow()
    # myMainWindow.show()
    # exit(app.exec_())