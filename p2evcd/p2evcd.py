# encoding:utf-8
# @Time     : 2020/4/15 14:08
# @Author   : Jerry Chou
# @File     : p2evcd.py
# @Function :
import datetime
from os.path import isdir, join, exists, basename, dirname
from os import makedirs, listdir, getcwd
import Pattern2EVCD_UI
from sys import argv, exit
from math import ceil

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QFileDialog

periodInNS = 41600  # ps
clkSignal = 'Unknown'  # clock pin
currentRowCount = 0
totalRowCount = 0
topLinePercent = 100
lineLimitCount = 1000
startTime = 0
collect_data = []
up_and_down = {'U': ['0', '6'], 'D': ['6', '0']}


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
                if fullname.endswith(postfix):
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


def GetSplitLimit(lineCount, topPercent):
    """
    get top percent line count if greater than lineLimitCount
    """
    if lineCount <= lineLimitCount:
        return lineCount
    elif lineCount * topPercent // 100 <= lineLimitCount:
        return GetSplitLimit(lineCount, topPercent + 1)
    else:
        return lineCount * topPercent // 100


def Parse(filePath, parseFolder, _signal):
    global currentRowCount
    cyc = 0
    stateTable = {'1': '1', '0': '0', 'X': 'x', 'L': '0', 'H': '1', 'Z': 'Z'}

    with open(filePath, 'r') as f:
        lines = f.readlines()

    signals = {}

    fileName = basename(filePath)
    limitLineCount = GetSplitLimit(len(lines), topLinePercent)
    parseFile = parseFolder + '/' + fileName + '_' + str(ceil(100 * limitLineCount / len(lines))) + '%.evcd'
    f = open(parseFile, 'w')
    f.write('$timescale\n')
    f.write(' 1ps\n')
    f.write('$end\n')
    f.write('\n')
    f.write('$scope module {0} $end\n'.format(fileName))
    f.write('\n')
    f.write('$scope module EVCD_Pannel $end\n')
    isFirstLine = True

    for lineNum in range(limitLineCount):
        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))
        if ',' in lines[lineNum]:
            pinList = lines[lineNum].strip().strip(';').split(',')
        elif '*' not in lines[lineNum]:
            continue
        else:
            if isFirstLine:
                if 'RPT' in lines[lineNum]:
                    RPTNum = int(lines[lineNum].split('RPT')[1].strip().split(';')[0])
                else:
                    RPTNum = 1
                firstLine = lines[lineNum].split('*')[1].strip()
                for i in range(len(pinList)):
                    signals[pinList[i]] = {'mark': '<' + str(i), 'state': stateTable[firstLine[i]], 'isClk': False}
                for signal in signals.keys():
                    f.write('$var wire       1 {0}    {1} $end\n'.format(signals[signal]['mark'], signal))
                f.write('$upscope $end\n')
                f.write('$upscope $end\n')
                f.write('$enddefinitions $end\n')
                f.write('$end\n')
                f.write('#0\n')
                cyc += 1
                if clkSignal != '':
                    signals[clkSignal]['isClk'] = True
                    for i in range(len(firstLine)):
                        if signals[pinList[i]]['isClk']:
                            f.write(
                                'p{0}	{1}	{2}	{3}\n'.format(collect_data[0], up_and_down[collect_data[0]][0],
                                                                     up_and_down[collect_data[0]][1],
                                                                     signals[clkSignal]['mark']))
                        else:
                            f.write('{0}{1}\n'.format(signals[pinList[i]]['state'], signals[pinList[i]]['mark']))
                        if i == len(firstLine) - 1 and signals[clkSignal]['state'] == '1':
                            collect_time = str(periodInNS * (cyc - 0.5))
                            f.write('#{0}\n'.format(collect_time))
                            f.write(
                                'p{0}	{1}	{2}	{3}\n'.format(collect_data[1], up_and_down[collect_data[1]][0],
                                                                     up_and_down[collect_data[1]][1],
                                                                     signals[clkSignal]['mark']))
                    if RPTNum > 1 and signals[clkSignal]['state'] == '1':
                        for i in range(1, RPTNum):
                            cyc += 1
                            f.write('#{0}\n'.format(str(periodInNS * (cyc - 1))))
                            collect_time = str(periodInNS * (cyc - 0.5))
                            f.write(
                                'p{0}	{1}	{2}	{3}\n'.format(collect_data[0], up_and_down[collect_data[0]][0],
                                                                     up_and_down[collect_data[0]][1],
                                                                     signals[clkSignal]['mark']))
                            f.write('#{0}\n'.format(collect_time))
                            f.write(
                                'p{0}	{1}	{2}	{3}\n'.format(collect_data[1], up_and_down[collect_data[1]][0],
                                                                     up_and_down[collect_data[1]][1],
                                                                     signals[clkSignal]['mark']))
                else:
                    for i in range(len(firstLine)):
                        f.write('{0}{1}\n'.format(signals[pinList[i]]['state'], signals[pinList[i]]['mark']))
                    cyc += (RPTNum - 1)
                isFirstLine = False
                continue
            if 'RPT' in lines[lineNum]:
                RPTNum = int(lines[lineNum].split('RPT')[1].split(';')[0].strip())
            else:
                RPTNum = 1
            line = lines[lineNum].split('*')[1].strip()
            printTime = False
            cyc += 1
            if clkSignal != '':
                for i in range(len(line)):
                    if signals[pinList[i]]['isClk']:
                        signals[pinList[i]]['state'] = stateTable[line[i]]
                    elif stateTable[line[i]] == signals[pinList[i]]['state'] and i < len(line) - 1:
                        continue
                    elif stateTable[line[i]] != signals[pinList[i]]['state']:
                        f.write('#{0}\n'.format(str(periodInNS * (cyc - 1))))
                        printTime = True
                        signals[pinList[i]]['state'] = stateTable[line[i]]
                        f.write('{0}{1}\n'.format(signals[pinList[i]]['state'], signals[pinList[i]]['mark']))
                    if i == len(line) - 1 and signals[clkSignal]['state'] == '1':
                        if not printTime:
                            f.write('#{0}\n'.format(str(periodInNS * (cyc - 1))))
                        collect_time = str(periodInNS * (cyc - 0.5))
                        f.write(
                            'p{0}	{1}	{2}	{3}\n'.format(collect_data[0], up_and_down[collect_data[0]][0],
                                                                 up_and_down[collect_data[0]][1],
                                                                 signals[clkSignal]['mark']))
                        f.write('#{0}\n'.format(collect_time))
                        f.write(
                            'p{0}	{1}	{2}	{3}\n'.format(collect_data[1], up_and_down[collect_data[1]][0],
                                                                 up_and_down[collect_data[1]][1],
                                                                 signals[clkSignal]['mark']))
                if RPTNum > 1 and signals[clkSignal]['state'] == '1':
                    for i in range(1, RPTNum):
                        cyc += 1
                        f.write('#{0}\n'.format(str(periodInNS * (cyc - 1))))
                        collect_time = str(periodInNS * (cyc - 0.5))
                        f.write(
                            'p{0}	{1}	{2}	{3}\n'.format(collect_data[0], up_and_down[collect_data[0]][0],
                                                                 up_and_down[collect_data[0]][1],
                                                                 signals[clkSignal]['mark']))
                        f.write('#{0}\n'.format(collect_time))
                        f.write(
                            'p{0}	{1}	{2}	{3}\n'.format(collect_data[1], up_and_down[collect_data[1]][0],
                                                                 up_and_down[collect_data[1]][1],
                                                                 signals[clkSignal]['mark']))
            else:
                for i in range(len(line)):
                    if stateTable[line[i]] == signals[pinList[i]]['state']:
                        continue
                    else:
                        if not printTime:
                            f.write('#{0}\n'.format(str(periodInNS * (cyc - 1))))
                            printTime = True
                        signals[pinList[i]]['state'] = stateTable[line[i]]
                        f.write('{0}{1}\n'.format(signals[pinList[i]]['state'], signals[pinList[i]]['mark']))
                cyc += (RPTNum - 1)
    if clkSignal != '' and signals[clkSignal]['state'] == '0':
        f.write('#{0}\n'.format(str(periodInNS * cyc)))
    f.close()


class RunThread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self, openPath, chooseRadio):
        super(RunThread, self).__init__()
        self.openPath = openPath
        self.chooseRadio = chooseRadio

    def __del__(self):
        self.wait()

    def run(self):
        if self.chooseRadio == 'PatFolder':
            patFolder = self.openPath
            fileList = GetFileList(self.openPath, '.pat')
            if not fileList:
                return
        else:
            fileList = [self.openPath]
            patFolder = dirname(self.openPath)

        analysisFolder = patFolder + '\parse'
        MkDir(analysisFolder)

        for file in fileList:
            Parse(file, analysisFolder, self._signal)
        self._signal.emit(str(100))


class MainWindow(QMainWindow, Pattern2EVCD_UI.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.cwd = getcwd()
        self.qe = QErrorMessage(self)
        self.PatFolder_radioButton.setChecked(True)
        self.Open_pushButton.clicked.connect(self.Open)
        self.Period_lineEdit.setValidator(QIntValidator())
        self.TopLinePercent_lineEdit.setValidator(QIntValidator())
        self.LineLimitCount_lineEdit.setValidator(QIntValidator())
        self.Analysis_pushButton.clicked.connect(self.Analysis)

    def Open(self):
        if self.SingleFile_radioButton.isChecked():
            fileNameChoose, fileType = QFileDialog.getOpenFileName(self, 'Select Pattern File', self.cwd,
                                                                   'Pattern Files(*.pat);;All Files(*)')
            if not fileNameChoose:
                return
            self.OpenPath_lineEdit.setText(fileNameChoose)
        else:
            dirChoose = QFileDialog.getExistingDirectory(self, 'Select Directory', self.cwd)
            if not dirChoose:
                return
            self.OpenPath_lineEdit.setText(dirChoose)

    def CallBackLog(self, msg):
        self.progressBar.setValue(int(msg))  # pass the thread's parameters to progressBar
        if msg == '100':
            self.Analysis_pushButton.setEnabled(True)
            costTime = str(datetime.datetime.now() - startTime)[:10]
            self.CostTime_label.setText('CostTime : ' + costTime)

    def Analysis(self):
        if not self.OpenPath_lineEdit.text():
            self.qe.showMessage('Path cannot be empty!')
            return
        if not self.Period_lineEdit.text():
            self.qe.showMessage('Period cannot be empty!')
            return
        if not self.TopLinePercent_lineEdit.text():
            self.qe.showMessage('TopLinePercent cannot be empty!')
            return
        if not self.LineLimitCount_lineEdit.text():
            self.qe.showMessage('LineLimitCount cannot be empty!')
            return
        else:
            global startTime, totalRowCount, topLinePercent, lineLimitCount, periodInNS, clkSignal, currentRowCount, collect_data
            startTime = datetime.datetime.now()
            totalRowCount = 0
            if self.PatFolder_radioButton.isChecked():
                fileList = GetFileList(self.OpenPath_lineEdit.text(), '.pat')
                if not fileList:
                    return
            else:
                fileList = [self.OpenPath_lineEdit.text()]
            topLinePercent = int(self.TopLinePercent_lineEdit.text())
            lineLimitCount = int(self.LineLimitCount_lineEdit.text())
            for file in fileList:
                with open(file) as f:
                    lines = f.readlines()
                    totalRowCount += GetSplitLimit(len(lines), topLinePercent)
            if totalRowCount == 0:
                self.qe.showMessage('The test data in open path is illegal.')
                return
            periodInNS = int(self.Period_lineEdit.text())
            clkSignal = self.ClockPinName_lineEdit.text()
            currentRowCount = 0
            if self.PatFolder_radioButton.isChecked():
                chooseRadio = self.PatFolder_radioButton.text()
            else:
                chooseRadio = self.SingleFile_radioButton.text()
            if self.Up_radioButton.isChecked():
                collect_data = ['D', 'U']
            else:
                collect_data = ['U', 'D']
            # create thread
            self.Analysis_pushButton.setEnabled(False)
            self.thread = RunThread(self.OpenPath_lineEdit.text(), chooseRadio)
            # connect signal
            self.thread._signal.connect(self.CallBackLog)
            self.thread.start()


if __name__ == '__main__':
    app = QApplication(argv)
    myMainWindow = MainWindow()
    myMainWindow.show()
    exit(app.exec_())
