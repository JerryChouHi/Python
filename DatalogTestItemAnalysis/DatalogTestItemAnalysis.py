# -*- coding: utf-8 -*-


import DatalogTestItemAnalysis_UI
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QErrorMessage, QFileDialog
from os.path import exists
from os import makedirs, getcwd
from sys import argv, exit
from csv import reader
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False
plt.switch_backend('agg')

currentCount = 0
totalCount = 0
last_test_item_column_num = 0
sigma = 3
dpi = 300


def create_directory(path):
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
        print('{} already exists.'.format(path))
        return False


def search_string(data, target):
    """
    find out if target exists in data
    :return: return index if find target,else return False
    """
    for i in range(len(data)):
        try:
            column_num = data[i].index(target)
            row_num = i
            return row_num, column_num
        except:
            pass
    print("Can't find " + str(target) + " !")
    return False


def auto_label(rects):
    for rect in rects:
        height = rect.get_height()
        x = rect.get_x() + rect.get_width() / 2.
        y = 1.02 * height
        plt.text(x, y, '%s' % height, fontsize=8, ha='center')


def get_pos(num):
    temp_num = int(abs(num))
    c = 0
    while temp_num != 0:
        temp_num = temp_num // 10
        c += 1
    return c


def Analysis(file, _signal):
    """
    Analysis csv file to generate 'filename_sigmaX/.png':
        generate a graph for each test item which high limit is not equal to low limit
    :param file: csv file to be analyzed
    :param _signal: signal to update progressBar
    :return: None
    """
    global currentCount
    with open(file) as f:
        data = []
        csvReader = reader(f)
        for row in csvReader:
            data.append(row)
    find_data = False
    for i in range(len(data)):
        if data[i][0] == 'ChipNo':
            test_item_row_num = i
        elif data[i][0] == 'MAX':
            high_limit_row_num = i
        elif data[i][0] == 'MIN':
            low_limit_row_num = i
        else:
            try:
                int(data[i][0])
                test_data_row_num = i
                for j in range(len(data[i])):
                    if type(eval(data[i][j])) == float:
                        test_data_column_num = j
                        find_data = True
                        break
            except:
                pass
        if find_data:
            break
    # get row of first register
    first_register_row_num = len(data)
    for i in range(test_data_row_num, len(data)):
        try:
            int(data[i][0])
        except:
            first_register_row_num = i
            break

    test_item_data = {}
    for col_num in range(test_data_column_num, last_test_item_column_num):
        test_item_name = data[test_item_row_num][col_num]
        high_limit_data = data[high_limit_row_num][col_num]
        try:
            float(high_limit_data)
            low_limit_data = data[low_limit_row_num][col_num]
            if float(low_limit_data) == float(high_limit_data):
                continue
            else:
                diff = float(high_limit_data) - float(low_limit_data)
                big_range = False
                if diff < 100:
                    round_value = 1
                    while diff * 10 < 1:
                        round_value += 1
                else:
                    big_range = True
                temp_data = []
                height = []
                for row_num in range(test_data_row_num, first_register_row_num):
                    value = data[row_num][col_num]
                    try:
                        float(value)
                        if big_range:
                            pos = get_pos(float(value))
                            temp_data.append(float(value) // pow(10, pos - 2) * pow(10, pos - 2))
                        else:
                            temp_data.append(round(float(value), round_value))
                    except:
                        continue
                mean_value = np.mean(temp_data)
                std_value = np.std(temp_data)
                threshold1 = mean_value - sigma * std_value
                threshold2 = mean_value + sigma * std_value
                hres_data = []
                for value in temp_data:
                    if threshold1 <= value <= threshold2:
                        hres_data.append(value)
                x = list(set(hres_data))
                x.sort()
                for num in x:
                    height.append(hres_data.count(num))
                test_item_data[test_item_name] = {'HiLimit': float(high_limit_data), 'LoLimit': float(low_limit_data),
                                                  'x': x, 'height': height}
        except:
            continue
    # save test item image
    imageFolder = file.replace('.csv', '_sigma' + str(sigma) + '_dpi' + str(dpi) + '/')
    create_directory(imageFolder)
    for test_item_name in test_item_data.keys():
        fig = plt.figure(figsize=(22, 10))
        rect = plt.bar(test_item_data[test_item_name]['x'], test_item_data[test_item_name]['height'],
                       width=1 / pow(10, round_value),
                       color='rgb')
        auto_label(rect)
        imagePath = imageFolder + test_item_name.replace('/', '_') + '.png'
        plt.plot([test_item_data[test_item_name]['LoLimit'], test_item_data[test_item_name]['LoLimit']],
                 [0, max(test_item_data[test_item_name]['height'])], color='blue', linestyle='-')
        plt.plot([test_item_data[test_item_name]['HiLimit'], test_item_data[test_item_name]['HiLimit']],
                 [0, max(test_item_data[test_item_name]['height'])], color='red', linestyle='-')
        center = (test_item_data[test_item_name]['HiLimit'] + test_item_data[test_item_name]['LoLimit']) / 2
        plt.plot([center, center], [0, max(test_item_data[test_item_name]['height'])], color='black',linestyle='--')
        plt.grid()
        plt.tick_params(labelsize=18)
        plt.savefig(imagePath, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
        currentCount += 1
        if currentCount != totalCount:
            _signal.emit(str(currentCount * 100 // totalCount))


class RunThread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self, openPath):
        super(RunThread, self).__init__()
        self.openPath = openPath

    def __del__(self):
        self.wait()

    def run(self):
        Analysis(self.openPath, self._signal)
        self._signal.emit(str(100))


class MainWindow(QMainWindow, DatalogTestItemAnalysis_UI.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.cwd = getcwd()
        self.qe = QErrorMessage(self)
        self.Open_pushButton.clicked.connect(self.Open)
        self.Run_pushButton.clicked.connect(self.Run)

    def Open(self):
        fileNameChoose, fileType = QFileDialog.getOpenFileName(self, 'Select CSV File', self.cwd,
                                                               'CSV Files(*.csv);;All Files(*)')
        if not fileNameChoose:
            return
        self.Open_lineEdit.setText(fileNameChoose)

    def CallBackLog(self, msg):
        self.progressBar.setValue(int(msg))  # pass the thread's parameters to progressBar
        if msg == '100':
            self.Run_pushButton.setEnabled(True)

    def Run(self):
        if not self.Open_lineEdit.text():
            self.qe.showMessage('Path cannot be empty!')
            return
        global totalCount, currentCount, last_test_item_column_num, sigma, dpi
        with open(self.Open_lineEdit.text()) as f:
            data = []
            csvReader = reader(f)
            for row in csvReader:
                data.append(row)
        # get row and column of last test item
        search_last_test_item = search_string(data, 'MIPIError')
        if not search_last_test_item:
            exit()
        else:
            last_test_item_column_num = search_last_test_item[1]
        totalCount = last_test_item_column_num
        currentCount = 0
        sigma = int(self.Sigma_lineEdit.text())
        dpi = int(self.DPI_lineEdit.text())
        # create thread
        self.Run_pushButton.setEnabled(False)
        self.thread = RunThread(self.Open_lineEdit.text())
        # connect signal
        self.thread._signal.connect(self.CallBackLog)
        self.thread.daemon = True
        self.thread.start()


if __name__ == '__main__':
    app = QApplication(argv)
    myMainWindow = MainWindow()
    myMainWindow.show()
    exit(app.exec_())
