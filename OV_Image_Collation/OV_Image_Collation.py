# encoding:utf-8
# @Time     : 2020/1/19 9:16
# @Author   : Jerry Chou
# @File     : OV_Image_Collation.py
# @Function :

from sys import argv, exit
from os import listdir, makedirs, getcwd
from os.path import isdir, join, exists, basename
from shutil import copy
import OV_Image_Collation_UI
from PyQt5.QtCore import  QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QErrorMessage
from re import match

barCount = 0


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


def MkDir(path):
    """
    create a folder
    """
    path = path.strip()
    path = path.rstrip("\\")
    isExists = exists(path)
    if not isExists:
        makedirs(path)
        return True
    else:
        return False


class Runthread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self, openPath):
        super(Runthread, self).__init__()
        self.openPath = openPath
        self.currentCount = 0

    def __del__(self):
        self.wait()

    def run(self):
        otpNames = listdir(self.openPath)

        # collation folder path
        if argv.count('-c') == 0:
            collationFolder = self.openPath + '_collation'
        else:
            collationFolder = argv[argv.index('-c') + 1]

        MkDir(collationFolder)

        otpFolders = []
        for otpName in otpNames:
            if isdir(join(self.openPath, otpName)):
                otpFolders.append(join(self.openPath, otpName))

        # classify raw files according to the image type in the file name
        pattern = '(\S+)_(\S+)-(\S+)_(\d+)_(\S+)_(\d+)x(\d+).raw'
        for i in range(len(otpFolders)):
            # get files under the folder
            fileList = GetFileList(otpFolders[i], '.raw')
            for file in fileList:
                fileName = basename(file)
                res = match(pattern,fileName)
                form = res[5]
                targetFolder = join(collationFolder, form)
                MkDir(targetFolder)
                copy(file,targetFolder)
                self.currentCount += 1
                if self.currentCount != barCount:
                    self._signal.emit(str(self.currentCount * 100 // barCount))
        self._signal.emit(str(100))


class MainWindow(QMainWindow, OV_Image_Collation_UI.Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.cwd = getcwd()
        self.qe = QErrorMessage(self)
        self.Open_pushButton.clicked.connect(self.Open)
        self.GatherData_pushButton.clicked.connect(self.GatherData)

    def Open(self):
        global barCount
        barCount = 0
        dirChoose = QFileDialog.getExistingDirectory(self, 'Select Directory', self.cwd)
        if not dirChoose:
            return
        self.OpenPath_lineEdit.setText(dirChoose)
        otpNames = listdir(dirChoose)

        otpFolders = []
        for otpName in otpNames:
            if isdir(join(dirChoose, otpName)):
                otpFolders.append(join(dirChoose, otpName))
        for i in range(len(otpFolders)):
            fileList = GetFileList(otpFolders[i], '.raw')
            barCount += len(fileList)

    def CallBackLog(self, msg):
        self.progressBar.setValue(int(msg))  # pass the thread's parameters to progressBar
        if msg == '100':
            self.GatherData_pushButton.setEnabled(True)

    def GatherData(self):
        if not self.OpenPath_lineEdit.text():
            self.qe.showMessage('Path cannot be empty!')
            return
        else:
            if barCount == 0:
                return
            # create thread
            self.GatherData_pushButton.setEnabled(False)
            self.thread = Runthread(self.OpenPath_lineEdit.text())
            # connect signal
            self.thread._signal.connect(self.CallBackLog)
            self.thread.start()

if __name__ == '__main__':
    app = QApplication(argv)
    myMainWindow = MainWindow()
    myMainWindow.show()
    exit(app.exec_())
