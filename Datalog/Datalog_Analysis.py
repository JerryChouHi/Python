# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Datalog_Analysis.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from Datalog_Analysis_UI import Ui_MainWindow
from sys import argv, exit, maxsize
from os import listdir, makedirs, getcwd
from csv import reader, field_size_limit
from PyQt5.QtCore import QThread, pyqtSignal, QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QErrorMessage
from os.path import join, isdir, exists, basename, dirname
from math import isnan
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Side, Border
from openpyxl.styles.colors import BLACK, WHITE, RED, GREEN
from openpyxl.utils import column_index_from_string, get_column_letter
from datetime import datetime
from numpy import array

thin = Side(border_style='thin', color=BLACK)
border = Border(top=thin, left=thin, right=thin, bottom=thin)

HiLimitRowNum = 0
LoLimitRowNum = 0
TestDataRowNum = 0
TestDataColLetter = 'A'
AllTestData = False
BeginColLetter = 'A'
EndColLetter = 'A'
RowCount = 0
CurrentRowCount = 0
# get current time
now_time = datetime.now().strftime("%Y%m%d%H%M%S")


def get_filelist(folder, postfix=None):
    """
    find a list of files with a postfix
    """
    fullname_list = []
    if isdir(folder):
        files = listdir(folder)
        for filename in files:
            fullname_list.append(join(folder, filename))
        if postfix:
            target_file_list = []
            for fullname in fullname_list:
                if fullname.endswith(postfix):
                    target_file_list.append(fullname)
            return target_file_list
        else:
            return fullname_list
    else:
        print("Error：Not a folder!")
        return False


def mkdir(path):
    """
    create a folder
    """
    path = path.strip()
    path = path.rstrip("\\")
    is_exists = exists(path)
    if not is_exists:
        makedirs(path)
        return True
    else:
        return False


def search_string(data, target):
    """
    find out if target exists in data
    """
    for i in range(len(data)):
        try:
            col_num = data[i].index(target)
            row_num = i
            return row_num, col_num
        except:
            pass
    print("Can't find " + target + " !")
    return False


def ParseAndSave(file, _signal, analysis_folder):
    """
    parse and save file
    """
    global CurrentRowCount
    data = []
    # get file data
    with open(file, encoding='unicode_escape') as f:
        csv_reader = reader(f)
        for row in csv_reader:
            data.append(row)

    # data check----------------------------
    row_count = len(data)

    datacheck_result = []
    for row_num in range(row_count):
        row_data = []
        OverLimitCount = 0
        for col_num in range(len(data[row_num])):
            value = data[row_num][col_num]
            high_limit_data = data[HiLimitRowNum - 1][col_num]
            low_limit_data = data[LoLimitRowNum - 1][col_num]
            if AllTestData:
                beginColNum = column_index_from_string(TestDataColLetter)
                endColNum = len(data[row_num])
            else:
                beginColNum = column_index_from_string(BeginColLetter)
                endColNum = column_index_from_string(EndColLetter)
            if col_num in range(beginColNum - 1, endColNum) and row_num in (HiLimitRowNum - 1, LoLimitRowNum - 1):
                # fill color of limit value is green
                row_data.append([value, GREEN])
            elif col_num in range(beginColNum - 1, endColNum) and row_num >= TestDataRowNum - 1:
                try:
                    value_convert = float(value)
                    try:
                        high_limit = float(high_limit_data)
                    except:
                        high_limit = high_limit_data
                    try:
                        low_limit = float(low_limit_data)
                    except:
                        low_limit = low_limit_data
                    if value_convert == int(value_convert):
                        value_convert = int(value_convert)
                    if high_limit == 'N' or (high_limit != 'N' and low_limit <= value_convert <= high_limit):
                        # fill color of following scenario value is white
                        # 1.limit is N
                        # 2.limit is not N and data wihtin limit
                        row_data.append([value_convert, WHITE])
                    else:
                        # fill color of over limit is red
                        row_data.append([value_convert, RED])
                        OverLimitCount += 1
                except:
                    if not value.strip():
                        # fill color of '' is purple
                        row_data.append([value, 'A020F0'])
                    elif not high_limit_data.strip():
                        # fill color is white
                        row_data.append([value, WHITE])
            else:
                # set '' when value is nan
                if isinstance(value, float) and isnan(value):
                    value = ''
                # fill color is white
                row_data.append([value, WHITE])
        if OverLimitCount > 0:
            row_data[0][0] = row_data[0][0] + '(' + str(OverLimitCount) + ')'
            row_data[0][1] = RED
        datacheck_result.append(row_data)
        CurrentRowCount += 1
        _signal.emit(str(CurrentRowCount * 100 // RowCount))

    file_name = basename(file).split('.')[0]
    data_check_file = join(analysis_folder, file_name + '_DataCheck_Analysis' + now_time + '.xlsx')
    data_check_wb = Workbook()  # create file object
    data_check_sheet = data_check_wb.active  # get first sheet
    freeze_panes = TestDataColLetter + str(TestDataRowNum)
    data_check_sheet.freeze_panes = freeze_panes  # set freeze panes

    irow = 1
    for i in range(len(datacheck_result)):
        for j in range(len(datacheck_result[i])):
            data_check_sheet.cell(row=irow, column=j + 1).value = datacheck_result[i][j][0]
            data_check_sheet.cell(row=irow, column=j + 1).fill = PatternFill(fill_type='solid',
                                                                             fgColor=datacheck_result[i][j][1])
            data_check_sheet.cell(row=irow, column=j + 1).border = border
        irow += 1
        CurrentRowCount += 1
        if CurrentRowCount != RowCount:
            _signal.emit(str(CurrentRowCount * 100 // RowCount))
    data_check_wb.save(data_check_file)


class Runthread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self, open_path, choose_radio):
        super(Runthread, self).__init__()
        self.open_path = open_path
        self.choose_radio = choose_radio

    def __del__(self):
        self.wait()

    def run(self):
        if self.choose_radio == 'DateFolder':
            lotno_names = listdir(self.open_path)
            for name in lotno_names:
                folder = join(self.open_path, name)
                if isdir(folder):
                    # get CSV file under the folder
                    file_list = get_filelist(folder, '.csv')

                    # create analysis folder
                    analysis_folder = folder + '\Analysis'
                    mkdir(analysis_folder)

                    for file in file_list:
                        ParseAndSave(file, self._signal, analysis_folder)
        elif self.choose_radio == 'LotFolder':
            # get CSV file under the folder
            file_list = get_filelist(self.open_path, '.csv')

            # create analysis folder
            analysis_folder = self.open_path + '\Analysis'
            mkdir(analysis_folder)

            for file in file_list:
                ParseAndSave(file, self._signal, analysis_folder)
        else:
            # create analysis folder
            analysis_folder = dirname(self.open_path) + '\Analysis'
            mkdir(analysis_folder)
            ParseAndSave(self.open_path, self._signal, analysis_folder)
        self._signal.emit(str(100))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.cwd = getcwd()
        self.qe = QErrorMessage(self)
        self.DateFolder_radioButton.setChecked(True)
        self.Open_pushButton.clicked.connect(self.Open)
        self.HiLimitRowNum_lineEdit.setValidator(QIntValidator())
        self.LoLimitRowNum_lineEdit.setValidator(QIntValidator())
        self.TestDataRowNum_lineEdit.setValidator(QIntValidator())
        reg = QRegExp('[A-Z]+')
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.TestDataColLetter_lineEdit.setValidator(pValidator)
        self.AllTestData_radioButton.setChecked(True)
        self.AllTestData_radioButton.toggled.connect(self.btnstate)
        self.BeginColLetter_lineEdit.setValidator(pValidator)
        self.EndColLetter_lineEdit.setValidator(pValidator)
        if self.AllTestData_radioButton.isChecked():
            self.BeginColLetter_lineEdit.setEnabled(False)
            self.EndColLetter_lineEdit.setEnabled(False)
        self.Analysis_pushButton.clicked.connect(self.analysis)

    def btnstate(self):
        if self.AllTestData_radioButton.isChecked():
            self.BeginColLetter_lineEdit.setEnabled(False)
            self.EndColLetter_lineEdit.setEnabled(False)
        else:
            self.BeginColLetter_lineEdit.setEnabled(True)
            self.EndColLetter_lineEdit.setEnabled(True)


    def Open(self):
        global RowCount
        RowCount = 0
        if self.SingleFile_radioButton.isChecked():
            fileName_choose, filetype = QFileDialog.getOpenFileName(self, 'Select CSV File', self.cwd,
                                                                    'CSV Files(*.csv);;All Files(*)')
            if not fileName_choose:
                return
            self.OpenPath_lineEdit.setText(fileName_choose)
            with open(fileName_choose, encoding='unicode_escape') as f:
                csv_reader = reader(f)
                RowCount += (array(list(csv_reader)).shape[0] * 2)
            getParaFile = fileName_choose
        else:
            dir_choose = QFileDialog.getExistingDirectory(self, 'Select Directory', self.cwd)
            if not dir_choose:
                return
            self.OpenPath_lineEdit.setText(dir_choose)
            if self.DateFolder_radioButton.isChecked():
                lotno_names = listdir(self.OpenPath_lineEdit.text())
                for name in lotno_names:
                    folder = join(self.OpenPath_lineEdit.text(), name)
                    if isdir(folder):
                        # get CSV file under the folder
                        file_list = get_filelist(folder, '.csv')
                        if not file_list:
                            return
                        for file in file_list:
                            getParaFile = file
                            with open(file, encoding='unicode_escape') as f:
                                csv_reader = reader(f)
                                RowCount += (array(list(csv_reader)).shape[0] * 2)
            elif self.LotFolder_radioButton.isChecked():
                file_list = get_filelist(self.OpenPath_lineEdit.text(), '.csv')
                if not file_list:
                    return
                for file in file_list:
                    getParaFile = file
                    with open(file, encoding='unicode_escape') as f:
                        csv_reader = reader(f)
                        RowCount += (array(list(csv_reader)).shape[0] * 2)
        data = []
        with open(getParaFile, encoding='unicode_escape') as f:
            csv_reader = reader(f)
            for row in csv_reader:
                data.append(row)
        for i in range(len(data)):
            if data[i][0] == 'MAX':
                self.HiLimitRowNum_lineEdit.setText(str(i + 1))
            elif data[i][0] == 'MIN':
                self.LoLimitRowNum_lineEdit.setText(str(i + 1))
            else:
                try:
                    int(data[i][0])
                    self.TestDataRowNum_lineEdit.setText(str(i + 1))
                    for j in range(len(data[i])):
                        if type(eval(data[i][j])) == float:
                            self.TestDataColLetter_lineEdit.setText(get_column_letter(j + 1))
                            return
                except:
                    pass

    def call_backlog(self, msg):
        self.progressBar.setValue(int(msg))  # pass the thread's parameters to progressBar
        if msg == '100':
            self.Analysis_pushButton.setEnabled(True)

    def analysis(self):
        if not self.OpenPath_lineEdit.text():
            self.qe.showMessage('Path cannot be empty!')
            return
        elif not self.HiLimitRowNum_lineEdit.text():
            self.qe.showMessage('HiLimitRowNum cannot be empty!Input limit:Integer only.')
            return
        elif not self.LoLimitRowNum_lineEdit.text():
            self.qe.showMessage('LoLimitRowNum cannot be empty!Input limit:Integer only.')
            return
        elif not self.TestDataRowNum_lineEdit.text():
            self.qe.showMessage('TestDataRowNum cannot be empty!Input limit:Integer only.')
            return
        elif not self.TestDataColLetter_lineEdit.text():
            self.qe.showMessage('TestDataColLetter cannot be empty!Input limit:Uppercase only.')
            return
        else:
            if RowCount == 0:
                self.qe.showMessage('The test data in open path is illegal.')
                return
            global HiLimitRowNum
            HiLimitRowNum = int(self.HiLimitRowNum_lineEdit.text())
            global LoLimitRowNum
            LoLimitRowNum = int(self.LoLimitRowNum_lineEdit.text())
            global TestDataRowNum
            TestDataRowNum = int(self.TestDataRowNum_lineEdit.text())
            global TestDataColLetter
            TestDataColLetter = self.TestDataColLetter_lineEdit.text()
            global AllTestData
            if self.AllTestData_radioButton.isChecked():
                AllTestData = True
            else:
                global BeginColLetter
                global EndColLetter
                BeginColLetter = self.BeginColLetter_lineEdit.text()
                EndColLetter = self.EndColLetter_lineEdit.text()
            if self.DateFolder_radioButton.isChecked():
                choose_radio = self.DateFolder_radioButton.text()
            elif self.LotFolder_radioButton.isChecked():
                choose_radio = self.LotFolder_radioButton.text()
            else:
                choose_radio = self.SingleFile_radioButton.text()
            # create thread
            self.Analysis_pushButton.setEnabled(False)
            self.thread = Runthread(self.OpenPath_lineEdit.text(), choose_radio)
            # connect signal
            self.thread._signal.connect(self.call_backlog)
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
