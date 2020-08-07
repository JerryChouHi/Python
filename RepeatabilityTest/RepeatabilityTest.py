# encoding:utf-8
# @Time     : 2019/9/10
# @Author   : Jerry Chou
# @File     :
# @Function :

from csv import reader, field_size_limit
from os import listdir, makedirs, getcwd
from os.path import join, isdir, exists, basename, dirname
import numpy as np
import csv
from datetime import datetime
from sys import argv, maxsize, exit
import RepeatabilityTest_UI
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QFileDialog

nowTime = 'Unknown'
totalRowCount = 0
currentRowCount = 0


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


def SearchString(data, target):
    """
    find out if target exists in data
    """
    for i in range(len(data)):
        try:
            colNum = data[i].index(target)
            rowNum = i
            return rowNum, colNum
        except:
            pass
    print("Can't find " + target + " !")
    return False


def CalData(data, rowNum1, rowNum2):
    """
    get max data from rowNum1 to rowNum2
    """
    maxValue = float(data[rowNum1][1])
    triggerCount = data[rowNum1][0]
    for rowNum in range(rowNum1 + 1, rowNum2):
        if float(data[rowNum][1]) > maxValue:
            maxValue = float(data[rowNum][1])
            triggerCount = data[rowNum][0]
    return triggerCount, maxValue * 1000


def DeleteContinuousDuplicateData(file, analysisFolder, _signal):
    """
    delete continuous duplicate data and save data to file
    """
    global currentRowCount
    data = []
    with open(file) as f:
        csvReader = reader(f)
        for row in csvReader:
            data.append(row)
    searchTriggerCount = SearchString(data, 'Trigger count')
    if not searchTriggerCount:
        exit()
    else:
        triggerCountRowNum = searchTriggerCount[0]
    result = []
    for row in range(len(data)):
        if row <= triggerCountRowNum:
            result.append(data[row])
        else:
            if row == triggerCountRowNum + 1:
                compareValue = data[row][1]
                tempData = data[row]
                continue
            if data[row][1] == compareValue:
                continue
            else:
                result.append(tempData)
                compareValue = data[row][1]
                tempData = data[row]
        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))
    fileName = basename(file).split('.')[0]
    analysisFile = join(analysisFolder, fileName + '_Analysis' + nowTime + '.csv')
    with open(analysisFile, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for line in result:
            writer.writerow(line)


def ParseAndSaveFile(file, analysisFolder, _signal):
    """
    calculate max data of each group data
    calculate min,max,mean,std,sixSigma,cp20,cp15 of all max data
    save calculate data
    """
    global currentRowCount
    data = []
    with open(file) as f:
        csvReader = reader(f)
        for row in csvReader:
            data.append(row)
    searchTriggerCount = SearchString(data, 'Trigger count')
    if not searchTriggerCount:
        exit()
    else:
        triggerCountRowNum = searchTriggerCount[0]
    result = []
    currentRowCount += triggerCountRowNum
    for rowNum in range(triggerCountRowNum + 1, len(data)):
        if rowNum == 0:
            if data[rowNum][2] == 'GO':
                groupStartRowNum = rowNum
        else:
            if data[rowNum - 1][2] != 'GO' and data[rowNum][2] == 'GO':
                groupStartRowNum = rowNum
            if data[rowNum - 1][2] == 'GO' and data[rowNum][2] != 'GO':
                GroupEndRowNum = rowNum
                result.append(CalData(data, groupStartRowNum, GroupEndRowNum))
        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))
    if data[triggerCountRowNum + 1][2] == 'GO':
        del result[0]
    maxList = []
    for item in result:
        maxList.append(item[1])
    minValue = np.min(maxList)
    maxValue = np.max(maxList)
    meanValue = np.mean(maxList)
    stdValue = np.std(maxList)
    sixSigma = 6 * stdValue
    cp20 = 40 / sixSigma
    cp15 = 30 / sixSigma

    fileName = basename(file).split('.')[0]
    analysisFile = join(analysisFolder, fileName + '_Analysis' + nowTime + '.csv')
    with open(analysisFile, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['trigger count', 'OUT(um)', '', 'min', 'max', 'average', '6 sigma', 'cp(20um)', 'cp(15um)'])
        for i in range(len(result)):
            line = [result[i][0], result[i][1]]
            if i == 0:
                line.extend(['', minValue, maxValue, meanValue, sixSigma, cp20, cp15])
            writer.writerow(line)


class RunThread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self, openPath, chooseRadio, deleteDuplicate):
        super(RunThread, self).__init__()
        self.openPath = openPath
        self.chooseRadio = chooseRadio
        self.deleteDuplicate = deleteDuplicate

    def __del__(self):
        self.wait()

    def run(self):
        if self.chooseRadio == 'SourceFolder':
            sourcefileFolder = self.openPath
            fileList = GetFileList(self.openPath, '.csv')
            if not fileList:
                return
        else:
            fileList = [self.openPath]
            sourcefileFolder = dirname(self.openPath)

        analysisFolder = sourcefileFolder + '\Analysis'
        MkDir(analysisFolder)

        for file in fileList:
            if self.deleteDuplicate:
                DeleteContinuousDuplicateData(file, analysisFolder, self._signal)
            else:
                ParseAndSaveFile(file, analysisFolder, self._signal)
        self._signal.emit(str(100))


class MainWindow(QMainWindow, RepeatabilityTest_UI.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.cwd = getcwd()
        self.qe = QErrorMessage(self)
        self.SourceFolder_radioButton.setChecked(True)
        self.Open_pushButton.clicked.connect(self.Open)
        self.Analysis_pushButton.clicked.connect(self.Analysis)

    def Open(self):
        if self.SingleFile_radioButton.isChecked():
            fileNameChoose, fileType = QFileDialog.getOpenFileName(self, 'Select CSV File', self.cwd,
                                                                   'CSV Files(*.csv);;All Files(*)')
            if not fileNameChoose:
                return
            self.OpenPath_lineEdit.setText(fileNameChoose)
        elif self.SourceFolder_radioButton.isChecked():
            dirChoose = QFileDialog.getExistingDirectory(self, 'Select Directory', self.cwd)
            if not dirChoose:
                return
            self.OpenPath_lineEdit.setText(dirChoose)
        else:
            self.qe.showMessage('Please choose SourceFolder or SingleFile.')
            return

    def CallBackLog(self, msg):
        self.progressBar.setValue(int(msg))  # pass the thread's parameters to progressBar
        if msg == '100':
            self.Analysis_pushButton.setEnabled(True)

    def Analysis(self):
        if not self.OpenPath_lineEdit.text():
            self.qe.showMessage('Path cannot be empty!')
            return
        else:
            global totalRowCount
            totalRowCount = 0
            if self.SourceFolder_radioButton.isChecked():
                fileList = GetFileList(self.OpenPath_lineEdit.text(), '.csv')
                if not fileList:
                    return
            else:
                fileList = [self.OpenPath_lineEdit.text()]
            for file in fileList:
                with open(file) as f:
                    csvReader = reader(f)
                    totalRowCount += (np.array(list(csvReader)).shape[0])
            if totalRowCount == 0:
                self.qe.showMessage('The test data in open path is illegal.')
                return
            global nowTime
            nowTime = datetime.now().strftime("%Y%m%d%H%M%S")
            global currentRowCount
            currentRowCount = 0
            if self.SourceFolder_radioButton.isChecked():
                chooseRadio = self.SourceFolder_radioButton.text()
            else:
                chooseRadio = self.SingleFile_radioButton.text()
            # create thread
            self.Analysis_pushButton.setEnabled(False)
            self.thread = RunThread(self.OpenPath_lineEdit.text(), chooseRadio,
                                    self.DeleteDuplicate_radioButton.isChecked())
            # connect signal
            self.thread._signal.connect(self.CallBackLog)
            self.thread.start()


if __name__ == '__main__':
    # _csv.Error:field larger than field limit(131072)
    maxInt = maxsize
    while True:
        try:
            field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)
    app = QApplication(argv)
    myMainWindow = MainWindow()
    myMainWindow.show()
    exit(app.exec_())
