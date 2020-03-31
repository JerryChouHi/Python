# encoding:utf-8
# @Time     : 2019/9/9 13:32
# @Author   : Jerry Chou
# @File     :
# @Function : Date data analysis

import Datalog_DateLot_Analysis_UI
from csv import reader, field_size_limit
from os.path import basename, isdir, join, exists
from os import listdir, makedirs, getcwd
from datetime import datetime
from math import isnan
from sys import argv, maxsize, exit
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QErrorMessage
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.styles.colors import YELLOW, GREEN, BLACK, WHITE, RED
from openpyxl.utils import get_column_letter
from numpy import array


def FindItem(itemList, value):
    """
    find value in item list
    """
    return [i for i, v in enumerate(itemList) if v == value]


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


def SetColumnWidth(sheet):
    """
    set column width
    """
    # get the maximum width of each column
    colWidth = [0.5] * sheet.max_column
    for row in range(sheet.max_row):
        for col in range(sheet.max_column):
            value = sheet.cell(row=row + 1, column=col + 1).value
            if value:
                width = len(str(value))
                if width > colWidth[col]:
                    colWidth[col] = width
    # set column width
    for i in range(len(colWidth)):
        colLettert = get_column_letter(i + 1)
        if colWidth[i] > 100:
            # set to 100 if col_width greater than 100
            sheet.column_dimensions[colLettert].width = 100
        else:
            sheet.column_dimensions[colLettert].width = colWidth[i] + 4


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


rowOffset = 5
colOffset = 4
highLimitRowNum = 0
# default project
project = 'Unknown'
analysisItem = 'Unknown'
# get current time
nowTime = 'Unknown'
alignment = Alignment(horizontal='center', vertical='center')
thin = Side(border_style='thin', color=BLACK)
border = Border(top=thin, left=thin, right=thin, bottom=thin)
totalRowCount = 0
currentRowCount = 0

hwbinToSwbin = {
    'F28': {
        1: {'SWBin': (1, 2), 'isPassBin': True},
        2: {'SWBin': (41, 42, 43, 44, 45, 53, 54, 55), 'isPassBin': True},
        4: {'SWBin': (23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 36, 39, 40, 70, 71, 72), 'isPassBin': False},
        5: {'SWBin': (5, 6, 7, 8, 9, 12, 96, 97, 98, 99), 'isPassBin': False},
        6: {'SWBin': (13, 14, 15, 35), 'isPassBin': False}
    },
    'JX828': {
        3: {'SWBin': (1, 2, 3), 'isPassBin': True},
        1: {'SWBin': (63, 64, 65, 89, 90, 94), 'isPassBin': True},
        2: {'SWBin': (53, 54, 73, 74), 'isPassBin': True},
        4: {'SWBin': (23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 36, 39, 40, 56, 57, 58, 75), 'isPassBin': False},
        5: {'SWBin': (5, 6, 7, 8, 9, 12, 93, 96, 98, 99), 'isPassBin': False},
        6: {'SWBin': (13, 14, 15, 35, 46, 47, 48, 51, 60), 'isPassBin': False}
    },
    'JX825': {
        3: {'SWBin': (2, 255), 'isPassBin': True},
        4: {'SWBin': (23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 36, 39, 40, 63, 64, 65), 'isPassBin': False},
        5: {'SWBin': (5, 6, 7, 8, 9, 12, 89), 'isPassBin': False},
        6: {'SWBin': (13, 14, 15, 35, 46, 48, 53, 54, 60), 'isPassBin': False},
        8: {'SWBin': (94, 96, 97, 98, 99), 'isPassBin': False}
    }
}

binDefinitionList = {
    'F28':
        {
            'PCLK_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'HSYNC_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'VSYNC_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'D9_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'D8_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'D7_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'D6_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'D5_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'D4_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'D3_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'D2_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'D1_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'D0_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'SCL_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'SDA_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'RSTB_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'PWDN_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'DVDD_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'VRamp_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'VH_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'VN1_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'EXCLK_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'PCLK_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'HSYNC_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'VSYNC_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D9_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D8_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D7_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D6_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D5_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D4_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D3_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D2_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D1_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D0_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'SCL_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'SDA_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'RSTB_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'PWDN_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'EXCLK_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'PCLK_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'HSYNC_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'VSYNC_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D9_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D8_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D7_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D6_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D5_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D4_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D3_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D2_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D1_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'D0_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'SCL_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'SDA_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'RSTB_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'PWDN_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'EXCLK_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 2},
            'iic_test': {'SWBin': 7, 'HWBin': 5, 'Priority': 3},
            'DVDD_voltage': {'SWBin': 9, 'HWBin': 5, 'Priority': 4},
            'VH_voltage': {'SWBin': 9, 'HWBin': 5, 'Priority': 5},
            'VN1_voltage': {'SWBin': 9, 'HWBin': 5, 'Priority': 6},
            'Active_AVDD': {'SWBin': 12, 'HWBin': 5, 'Priority': 7},
            'Active_DOVDD': {'SWBin': 12, 'HWBin': 5, 'Priority': 8},
            'PWDN_AVDD': {'SWBin': 8, 'HWBin': 5, 'Priority': 9},
            'PWDN_DOVDD': {'SWBin': 8, 'HWBin': 5, 'Priority': 10},
            'PWDN_Total': {'SWBin': 8, 'HWBin': 5, 'Priority': 11},
            'PLCK_Freq': {'SWBin': 9, 'HWBin': 5, 'Priority': 12},
            'BK_ImageCapture': {'SWBin': 98, 'HWBin': 5, 'Priority': 13},
            'BK_ImageCalculation': {'SWBin': 97, 'HWBin': 5, 'Priority': 14},
            'BLC_R': {'SWBin': 7, 'HWBin': 5, 'Priority': 15},
            'BLC_Gr': {'SWBin': 7, 'HWBin': 5, 'Priority': 15},
            'BLC_Gb': {'SWBin': 7, 'HWBin': 5, 'Priority': 15},
            'BLC_B': {'SWBin': 7, 'HWBin': 5, 'Priority': 15},
            'BK_DeadRowExBPix_R': {'SWBin': 15, 'HWBin': 6, 'Priority': 16, 'IsNan': 'BK_ImageCapture'},
            'BK_DeadRowExBPix_Gr': {'SWBin': 15, 'HWBin': 6, 'Priority': 16, 'IsNan': 'BK_ImageCapture'},
            'BK_DeadRowExBPix_Gb': {'SWBin': 15, 'HWBin': 6, 'Priority': 16, 'IsNan': 'BK_ImageCapture'},
            'BK_DeadRowExBPix_B': {'SWBin': 15, 'HWBin': 6, 'Priority': 16, 'IsNan': 'BK_ImageCapture'},
            'BK_DeadColExBPix_R': {'SWBin': 14, 'HWBin': 6, 'Priority': 17, 'IsNan': 'BK_ImageCapture'},
            'BK_DeadColExBPix_Gr': {'SWBin': 14, 'HWBin': 6, 'Priority': 17, 'IsNan': 'BK_ImageCapture'},
            'BK_DeadColExBPix_Gb': {'SWBin': 14, 'HWBin': 6, 'Priority': 17, 'IsNan': 'BK_ImageCapture'},
            'BK_DeadColExBPix_B': {'SWBin': 14, 'HWBin': 6, 'Priority': 17, 'IsNan': 'BK_ImageCapture'},
            'BK_Mean_R': {'SWBin': 13, 'HWBin': 6, 'Priority': 18, 'IsNan': 'BK_ImageCapture'},
            'BK_Mean_Gr': {'SWBin': 13, 'HWBin': 6, 'Priority': 19, 'IsNan': 'BK_ImageCapture'},
            'BK_Mean_Gb': {'SWBin': 13, 'HWBin': 6, 'Priority': 20, 'IsNan': 'BK_ImageCapture'},
            'BK_Mean_B': {'SWBin': 13, 'HWBin': 6, 'Priority': 21, 'IsNan': 'BK_ImageCapture'},
            'BK_StdDEV_R': {'SWBin': 13, 'HWBin': 6, 'Priority': 22, 'IsNan': 'BK_ImageCapture'},
            'BK_StdDEV_Gr': {'SWBin': 13, 'HWBin': 6, 'Priority': 23, 'IsNan': 'BK_ImageCapture'},
            'BK_StdDEV_Gb': {'SWBin': 13, 'HWBin': 6, 'Priority': 24, 'IsNan': 'BK_ImageCapture'},
            'BK_StdDEV_B': {'SWBin': 13, 'HWBin': 6, 'Priority': 25, 'IsNan': 'BK_ImageCapture'},
            'LT_ImageCapture': {'SWBin': 99, 'HWBin': 5, 'Priority': 26},
            'LT_ImageCalculation': {'SWBin': 97, 'HWBin': 5, 'Priority': 27},
            'LT_DRow_R': {'SWBin': 25, 'HWBin': 4, 'Priority': 28, 'IsNan': 'LT_ImageCapture'},
            'LT_DRow_Gr': {'SWBin': 25, 'HWBin': 4, 'Priority': 28, 'IsNan': 'LT_ImageCapture'},
            'LT_DRow_Gb': {'SWBin': 25, 'HWBin': 4, 'Priority': 28, 'IsNan': 'LT_ImageCapture'},
            'LT_DRow_B': {'SWBin': 25, 'HWBin': 4, 'Priority': 28, 'IsNan': 'LT_ImageCapture'},
            'LT_DCol_R': {'SWBin': 24, 'HWBin': 4, 'Priority': 29, 'IsNan': 'LT_ImageCapture'},
            'LT_DCol_Gr': {'SWBin': 24, 'HWBin': 4, 'Priority': 29, 'IsNan': 'LT_ImageCapture'},
            'LT_DCol_Gb': {'SWBin': 24, 'HWBin': 4, 'Priority': 29, 'IsNan': 'LT_ImageCapture'},
            'LT_DCol_B': {'SWBin': 24, 'HWBin': 4, 'Priority': 29, 'IsNan': 'LT_ImageCapture'},
            'LT_DRow_Color': {'SWBin': 25, 'HWBin': 4, 'Priority': 30, 'IsNan': 'LT_ImageCapture'},
            'LT_DCol_Color': {'SWBin': 24, 'HWBin': 4, 'Priority': 31, 'IsNan': 'LT_ImageCapture'},
            'LT_Mean_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 32, 'IsNan': 'LT_ImageCapture'},
            'LT_Mean_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 33, 'IsNan': 'LT_ImageCapture'},
            'LT_Mean_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 34, 'IsNan': 'LT_ImageCapture'},
            'LT_Mean_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 35, 'IsNan': 'LT_ImageCapture'},
            'LT_StdDEV_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 36, 'IsNan': 'LT_ImageCapture'},
            'LT_StdDEV_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 37, 'IsNan': 'LT_ImageCapture'},
            'LT_StdDEV_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 38, 'IsNan': 'LT_ImageCapture'},
            'LT_StdDEV_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 39, 'IsNan': 'LT_ImageCapture'},
            'LT_RI_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 40, 'IsNan': 'LT_ImageCapture'},
            'LT_RI_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 41, 'IsNan': 'LT_ImageCapture'},
            'LT_RI_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 42, 'IsNan': 'LT_ImageCapture'},
            'LT_RI_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 43, 'IsNan': 'LT_ImageCapture'},
            'LT_Ratio_GrR': {'SWBin': 23, 'HWBin': 4, 'Priority': 44, 'IsNan': 'LT_ImageCapture'},
            'LT_Ratio_GbR': {'SWBin': 23, 'HWBin': 4, 'Priority': 45, 'IsNan': 'LT_ImageCapture'},
            'LT_Ratio_GrB': {'SWBin': 23, 'HWBin': 4, 'Priority': 46, 'IsNan': 'LT_ImageCapture'},
            'LT_Ratio_GbB': {'SWBin': 23, 'HWBin': 4, 'Priority': 47, 'IsNan': 'LT_ImageCapture'},
            'LT_Ratio_GbGr': {'SWBin': 23, 'HWBin': 4, 'Priority': 48, 'IsNan': 'LT_ImageCapture'},
            'LT_LostBit': {'SWBin': 23, 'HWBin': 4, 'Priority': 49, 'IsNan': 'LT_ImageCapture'},
            'LT_LostBitSNR_SumDIFF_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 50, 'IsNan': 'LT_ImageCapture'},
            'LT_LostBitSNR_SumDIFF_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 51, 'IsNan': 'LT_ImageCapture'},
            'LT_LostBitSNR_SumDIFF_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 52, 'IsNan': 'LT_ImageCapture'},
            'LT_LostBitSNR_SumDIFF_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 53, 'IsNan': 'LT_ImageCapture'},
            'LB_LT_ImageCapture': {'SWBin': 99, 'HWBin': 5, 'Priority': 54},
            'LB_LT_ImageCalculation': {'SWBin': 97, 'HWBin': 5, 'Priority': 55},
            'LB_LT_Mean_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 56, 'IsNan': 'LB_LT_ImageCapture'},
            'LB_LT_Mean_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 57, 'IsNan': 'LB_LT_ImageCapture'},
            'LB_LT_Mean_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 58, 'IsNan': 'LB_LT_ImageCapture'},
            'LB_LT_Mean_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 59, 'IsNan': 'LB_LT_ImageCapture'},
            'LB_LT_LostBit': {'SWBin': 23, 'HWBin': 4, 'Priority': 60, 'IsNan': 'LB_LT_ImageCapture'},
            'LB_LT_LostBitSNR_SumDIFF_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 61, 'IsNan': 'LB_LT_ImageCapture'},
            'LB_LT_LostBitSNR_SumDIFF_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 62, 'IsNan': 'LB_LT_ImageCapture'},
            'LB_LT_LostBitSNR_SumDIFF_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 63, 'IsNan': 'LB_LT_ImageCapture'},
            'LB_LT_LostBitSNR_SumDIFF_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 64, 'IsNan': 'LB_LT_ImageCapture'},
            'FW_LT_ImageCapture': {'SWBin': 99, 'HWBin': 5, 'Priority': 65},
            'FW_LT_Calculation': {'SWBin': 97, 'HWBin': 5, 'Priority': 66},
            'FW_LT_DRow_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 67, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_DRow_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 67, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_DRow_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 67, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_DRow_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 67, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_DCol_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 68, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_DCol_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 68, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_DCol_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 68, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_DCol_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 68, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_DRow_Color': {'SWBin': 36, 'HWBin': 4, 'Priority': 69, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_DCol_Color': {'SWBin': 36, 'HWBin': 4, 'Priority': 70, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_Mean_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 77, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_Mean_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 78, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_Mean_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 79, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_Mean_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 80, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_StdDEV_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 81, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_StdDEV_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 82, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_StdDEV_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 83, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_StdDEV_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 84, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_RI_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 85, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_RI_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 86, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_RI_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 87, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_RI_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 88, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_Ratio_GrR': {'SWBin': 36, 'HWBin': 4, 'Priority': 89, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_Ratio_GbR': {'SWBin': 36, 'HWBin': 4, 'Priority': 90, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_Ratio_GrB': {'SWBin': 36, 'HWBin': 4, 'Priority': 91, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_Ratio_GbB': {'SWBin': 36, 'HWBin': 4, 'Priority': 92, 'IsNan': 'FW_LT_ImageCapture'},
            'FW_LT_Ratio_GbGr': {'SWBin': 36, 'HWBin': 4, 'Priority': 93, 'IsNan': 'FW_LT_ImageCapture'},
            'LT_CornerLine': {'SWBin': 26, 'HWBin': 4, 'Priority': 94},
            'LT_ScratchLine': {'SWBin': 26, 'HWBin': 4, 'Priority': 95},
            'LT_Blemish': {'SWBin': 31, 'HWBin': 4, 'Priority': 96},
            'LT_LineStripe': {'SWBin': 27, 'HWBin': 4, 'Priority': 97},
            'LT_Particle': {'SWBin': 32, 'HWBin': 4, 'Priority': 98},
            'BK_Cluster2': {'SWBin': 30, 'HWBin': 4, 'Priority': 99},
            'LT_Cluster2': {'SWBin': 30, 'HWBin': 4, 'Priority': 100},
            'BK_Cluster1': {'SWBin': 29, 'HWBin': 4, 'Priority': 101},
            'LT_Cluster1': {'SWBin': 29, 'HWBin': 4, 'Priority': 102},
            'WP_Count': {'SWBin': 35, 'HWBin': 6, 'Priority': 103},
            'BK_Cluster3GrGb': {'SWBin': 39, 'HWBin': 4, 'Priority': 104},
            'LT_Cluster3GrGb': {'SWBin': 40, 'HWBin': 4, 'Priority': 105},
            'BK_Cluster3SubtractGrGb': {'SWBin': 33, 'HWBin': 4, 'Priority': 106},
            'LT_Cluster3SubtractGrGb': {'SWBin': 34, 'HWBin': 4, 'Priority': 107},
            'LB_BK_DeadRowExBPix_R': {'SWBin': 45, 'HWBin': 2, 'Priority': 108},
            'LB_BK_DeadRowExBPix_Gr': {'SWBin': 45, 'HWBin': 2, 'Priority': 108},
            'LB_BK_DeadRowExBPix_Gb': {'SWBin': 45, 'HWBin': 2, 'Priority': 108},
            'LB_BK_DeadRowExBPix_B': {'SWBin': 45, 'HWBin': 2, 'Priority': 108},
            'LB_BK_DeadColExBPix_R': {'SWBin': 44, 'HWBin': 2, 'Priority': 109},
            'LB_BK_DeadColExBPix_Gr': {'SWBin': 44, 'HWBin': 2, 'Priority': 109},
            'LB_BK_DeadColExBPix_Gb': {'SWBin': 44, 'HWBin': 2, 'Priority': 109},
            'LB_BK_DeadColExBPix_B': {'SWBin': 44, 'HWBin': 2, 'Priority': 109},
            'SR_LT_ImageCapture': {'SWBin': 96, 'HWBin': 5, 'Priority': 110},
            'SR_LT_Calculation': {'SWBin': 97, 'HWBin': 5, 'Priority': 110},
            'SR_LT_DRow_R': {'SWBin': 55, 'HWBin': 2, 'Priority': 111, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_DRow_Gr': {'SWBin': 55, 'HWBin': 2, 'Priority': 111, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_DRow_Gb': {'SWBin': 55, 'HWBin': 2, 'Priority': 111, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_DRow_B': {'SWBin': 55, 'HWBin': 2, 'Priority': 111, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_DCol_R': {'SWBin': 54, 'HWBin': 2, 'Priority': 112, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_DCol_Gr': {'SWBin': 54, 'HWBin': 2, 'Priority': 112, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_DCol_Gb': {'SWBin': 54, 'HWBin': 2, 'Priority': 112, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_DCol_B': {'SWBin': 54, 'HWBin': 2, 'Priority': 112, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_DRow_Color': {'SWBin': 55, 'HWBin': 2, 'Priority': 113, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_DCol_Color': {'SWBin': 54, 'HWBin': 2, 'Priority': 114, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_Mean_R': {'SWBin': 53, 'HWBin': 2, 'Priority': 115, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_Mean_Gr': {'SWBin': 53, 'HWBin': 2, 'Priority': 116, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_Mean_Gb': {'SWBin': 53, 'HWBin': 2, 'Priority': 117, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_Mean_B': {'SWBin': 53, 'HWBin': 2, 'Priority': 118, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_StdDEV_R': {'SWBin': 53, 'HWBin': 2, 'Priority': 119, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_StdDEV_Gr': {'SWBin': 53, 'HWBin': 2, 'Priority': 120, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_StdDEV_Gb': {'SWBin': 53, 'HWBin': 2, 'Priority': 121, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_StdDEV_B': {'SWBin': 53, 'HWBin': 2, 'Priority': 122, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_RI_R': {'SWBin': 53, 'HWBin': 2, 'Priority': 123, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_RI_Gr': {'SWBin': 53, 'HWBin': 2, 'Priority': 124, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_RI_Gb': {'SWBin': 53, 'HWBin': 2, 'Priority': 125, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_RI_B': {'SWBin': 53, 'HWBin': 2, 'Priority': 126, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_Ratio_GrR': {'SWBin': 53, 'HWBin': 2, 'Priority': 127, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_Ratio_GbR': {'SWBin': 53, 'HWBin': 2, 'Priority': 128, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_Ratio_GrB': {'SWBin': 53, 'HWBin': 2, 'Priority': 129, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_Ratio_GbB': {'SWBin': 53, 'HWBin': 2, 'Priority': 130, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_Ratio_GbGr': {'SWBin': 53, 'HWBin': 2, 'Priority': 131, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_LT_LostBit': {'SWBin': 53, 'HWBin': 2, 'Priority': 132, 'IsNan': 'SR_LT_ImageCapture'},
            'SR_BK_ImageCapture': {'SWBin': 96, 'HWBin': 5, 'Priority': 133},
            'SR_BK_Calculation': {'SWBin': 97, 'HWBin': 5, 'Priority': 134},
            'SR_BK_DeadRowExBPix_R': {'SWBin': 42, 'HWBin': 2, 'Priority': 135, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_DeadRowExBPix_Gr': {'SWBin': 42, 'HWBin': 2, 'Priority': 135, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_DeadRowExBPix_Gb': {'SWBin': 42, 'HWBin': 2, 'Priority': 135, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_DeadRowExBPix_B': {'SWBin': 42, 'HWBin': 2, 'Priority': 135, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_DeadColExBPix_R': {'SWBin': 41, 'HWBin': 2, 'Priority': 136, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_DeadColExBPix_Gr': {'SWBin': 41, 'HWBin': 2, 'Priority': 136, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_DeadColExBPix_Gb': {'SWBin': 41, 'HWBin': 2, 'Priority': 136, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_DeadColExBPix_B': {'SWBin': 41, 'HWBin': 2, 'Priority': 136, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_Mean_R': {'SWBin': 43, 'HWBin': 2, 'Priority': 137, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_Mean_Gr': {'SWBin': 43, 'HWBin': 2, 'Priority': 138, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_Mean_Gb': {'SWBin': 43, 'HWBin': 2, 'Priority': 139, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_Mean_B': {'SWBin': 43, 'HWBin': 2, 'Priority': 140, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_StdDEV_R': {'SWBin': 43, 'HWBin': 2, 'Priority': 141, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_StdDEV_Gr': {'SWBin': 43, 'HWBin': 2, 'Priority': 142, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_StdDEV_Gb': {'SWBin': 43, 'HWBin': 2, 'Priority': 143, 'IsNan': 'SR_BK_ImageCapture'},
            'SR_BK_StdDEV_B': {'SWBin': 43, 'HWBin': 2, 'Priority': 144, 'IsNan': 'SR_BK_ImageCapture'},
            'Regular Line Pattern Change Fail': {'SWBin': 70, 'HWBin': 4, 'Priority': 145},  # not use
            'Diffuser2_LT_ImageCapture': {'SWBin': 99, 'HWBin': 5, 'Priority': 146},
            'Diffuser2_LT_Calculation': {'SWBin': 97, 'HWBin': 5, 'Priority': 147},
            'Diffuser2_LT_WeakLineRow_R': {'SWBin': 72, 'HWBin': 4, 'Priority': 148,
                                           'IsNan': 'Diffuser2_LT_ImageCapture'},
            'Diffuser2_LT_WeakLineRow_Gr': {'SWBin': 72, 'HWBin': 4, 'Priority': 148,
                                            'IsNan': 'Diffuser2_LT_ImageCapture'},
            'Diffuser2_LT_WeakLineRow_Gb': {'SWBin': 72, 'HWBin': 4, 'Priority': 148,
                                            'IsNan': 'Diffuser2_LT_ImageCapture'},
            'Diffuser2_LT_WeakLineRow_B': {'SWBin': 72, 'HWBin': 4, 'Priority': 148,
                                           'IsNan': 'Diffuser2_LT_ImageCapture'},
            'Diffuser2_LT_WeakLineCol_R': {'SWBin': 71, 'HWBin': 4, 'Priority': 149,
                                           'IsNan': 'Diffuser2_LT_ImageCapture'},
            'Diffuser2_LT_WeakLineCol_Gr': {'SWBin': 71, 'HWBin': 4, 'Priority': 149,
                                            'IsNan': 'Diffuser2_LT_ImageCapture'},
            'Diffuser2_LT_WeakLineCol_Gb': {'SWBin': 71, 'HWBin': 4, 'Priority': 149,
                                            'IsNan': 'Diffuser2_LT_ImageCapture'},
            'Diffuser2_LT_WeakLineCol_B': {'SWBin': 71, 'HWBin': 4, 'Priority': 149,
                                           'IsNan': 'Diffuser2_LT_ImageCapture'},
            'Binning': {'SWBin': 2, 'HWBin': 1, 'Priority': 145},
            'All Pass': {'SWBin': 1, 'HWBin': 1, 'Priority': 146}
        },
    'JX828':
        {
            'VSYNC_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'HSYNC_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 2},
            'PCLK_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 3},
            'EXCLK_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 4},
            'RSTB_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 5},
            'PWDN_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 6},
            'SDA_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 7},
            'SCL_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 8},
            'D0_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 9},
            'D1_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 10},
            'D2_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 11},
            'D3_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 12},
            'D4_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 13},
            'D5_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 14},
            'D6_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 15},
            'D7_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 16},
            'D8_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 17},
            'D9_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 18},
            'MCP_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 19},
            'MCN_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 20},
            'MDP0_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 21},
            'MDN0_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 22},
            'MDP1_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 23},
            'MDN1_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 24},
            'AVDD_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 25},
            'DOVDD_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 26},
            'VRamp_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 27},
            'VH_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 28},
            'VN1_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 29},
            'VSYNC_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 30},
            'HSYNC_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 31},
            'PCLK_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 32},
            'EXCLK_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 33},
            'RSTB_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 34},
            'PWDN_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 35},
            'SDA_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 36},
            'SCL_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 37},
            'D0_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 38},
            'D1_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 39},
            'D2_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 40},
            'D4_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 41},
            'D5_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 42},
            'D3_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 43},
            'D6_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 44},
            'D7_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 45},
            'D8_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 46},
            'D9_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 47},
            'MCP_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 48},
            'MCN_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 49},
            'MDP0_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 50},
            'MDN0_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 51},
            'MDP1_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 52},
            'MDN1_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 53},
            'VSYNC_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 54},
            'HSYNC_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 55},
            'PCLK_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 56},
            'EXCLK_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 57},
            'RSTB_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 58},
            'PWDN_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 59},
            'SDA_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 60},
            'SCL_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 61},
            'D0_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 62},
            'D1_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 63},
            'D2_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 64},
            'D4_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 65},
            'D5_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 66},
            'D3_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 67},
            'D6_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 68},
            'D7_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 69},
            'D8_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 70},
            'D9_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 71},
            'MCP_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 72},
            'MCN_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 73},
            'MDP0_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 74},
            'MDN0_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 75},
            'MDP1_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 76},
            'MDN1_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 77},
            'iic_test': {'SWBin': 7, 'HWBin': 5, 'Priority': 78},
            'DVDD_voltage': {'SWBin': 9, 'HWBin': 5, 'Priority': 79},
            'VH_voltage': {'SWBin': 9, 'HWBin': 5, 'Priority': 80},
            'VN1_voltage': {'SWBin': 9, 'HWBin': 5, 'Priority': 81},
            'Active_AVDD': {'SWBin': 12, 'HWBin': 5, 'Priority': 82},
            'Active_DOVDD': {'SWBin': 12, 'HWBin': 5, 'Priority': 83},
            'PWDN_AVDD': {'SWBin': 8, 'HWBin': 5, 'Priority': 84},
            'PWDN_DOVDD': {'SWBin': 8, 'HWBin': 5, 'Priority': 85},
            'PWDN_Total': {'SWBin': 8, 'HWBin': 5, 'Priority': 86},
            'DVP27M30F_BK_Cap': {'SWBin': 98, 'HWBin': 5, 'Priority': 87},
            'DVP27M30F_BK_Calc': {'SWBin': 97, 'HWBin': 5, 'Priority': 88},
            'DVP27M30F_BK_REG_VRamp': {'SWBin': 7, 'HWBin': 5, 'Priority': 89},
            'BLC_R': {'SWBin': 7, 'HWBin': 5, 'Priority': 90},
            'BLC_Gr': {'SWBin': 7, 'HWBin': 5, 'Priority': 91},
            'BLC_Gb': {'SWBin': 7, 'HWBin': 5, 'Priority': 92},
            'BLC_B': {'SWBin': 7, 'HWBin': 5, 'Priority': 93},
            'BK_DeadRowExBPix_R': {'SWBin': 15, 'HWBin': 6, 'Priority': 94, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_DeadRowExBPix_Gr': {'SWBin': 15, 'HWBin': 6, 'Priority': 95, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_DeadRowExBPix_Gb': {'SWBin': 15, 'HWBin': 6, 'Priority': 96, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_DeadRowExBPix_B': {'SWBin': 15, 'HWBin': 6, 'Priority': 97, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_DeadColExBPix_R': {'SWBin': 14, 'HWBin': 6, 'Priority': 98, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_DeadColExBPix_Gr': {'SWBin': 14, 'HWBin': 6, 'Priority': 99, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_DeadColExBPix_Gb': {'SWBin': 14, 'HWBin': 6, 'Priority': 100, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_DeadColExBPix_B': {'SWBin': 14, 'HWBin': 6, 'Priority': 101, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VfpnQty_R': {'SWBin': 14, 'HWBin': 6, 'Priority': 102, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VfpnQty_Gr': {'SWBin': 14, 'HWBin': 6, 'Priority': 103, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VfpnQty_Gb': {'SWBin': 14, 'HWBin': 6, 'Priority': 104, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VfpnQty_B': {'SWBin': 14, 'HWBin': 6, 'Priority': 105, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue0_R': {'SWBin': 14, 'HWBin': 6, 'Priority': 106, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue0_Gr': {'SWBin': 14, 'HWBin': 6, 'Priority': 107, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue0_Gb': {'SWBin': 14, 'HWBin': 6, 'Priority': 108, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue0_B': {'SWBin': 14, 'HWBin': 6, 'Priority': 109, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue1_R': {'SWBin': 14, 'HWBin': 6, 'Priority': 110, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue1_Gr': {'SWBin': 14, 'HWBin': 6, 'Priority': 111, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue1_Gb': {'SWBin': 14, 'HWBin': 6, 'Priority': 112, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue1_B': {'SWBin': 14, 'HWBin': 6, 'Priority': 113, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue2_R': {'SWBin': 14, 'HWBin': 6, 'Priority': 114, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue2_Gr': {'SWBin': 14, 'HWBin': 6, 'Priority': 115, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue2_Gb': {'SWBin': 14, 'HWBin': 6, 'Priority': 116, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue2_B': {'SWBin': 14, 'HWBin': 6, 'Priority': 117, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue3_R': {'SWBin': 14, 'HWBin': 6, 'Priority': 118, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue3_Gr': {'SWBin': 14, 'HWBin': 6, 'Priority': 119, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue3_Gb': {'SWBin': 14, 'HWBin': 6, 'Priority': 120, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue3_B': {'SWBin': 14, 'HWBin': 6, 'Priority': 121, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue4_R': {'SWBin': 14, 'HWBin': 6, 'Priority': 122, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue4_Gr': {'SWBin': 14, 'HWBin': 6, 'Priority': 123, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue4_Gb': {'SWBin': 14, 'HWBin': 6, 'Priority': 124, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue4_B': {'SWBin': 14, 'HWBin': 6, 'Priority': 125, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_Mean_R': {'SWBin': 13, 'HWBin': 6, 'Priority': 126, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_Mean_Gr': {'SWBin': 13, 'HWBin': 6, 'Priority': 127, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_Mean_Gb': {'SWBin': 13, 'HWBin': 6, 'Priority': 128, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_Mean_B': {'SWBin': 13, 'HWBin': 6, 'Priority': 129, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_StdDEV_R': {'SWBin': 13, 'HWBin': 6, 'Priority': 130, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_StdDEV_Gr': {'SWBin': 13, 'HWBin': 6, 'Priority': 131, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_StdDEV_Gb': {'SWBin': 13, 'HWBin': 6, 'Priority': 132, 'IsNan': 'DVP27M30F_BK_Cap'},
            'BK_StdDEV_B': {'SWBin': 13, 'HWBin': 6, 'Priority': 133, 'IsNan': 'DVP27M30F_BK_Cap'},
            'DVP27M30F_LT_Cap': {'SWBin': 99, 'HWBin': 5, 'Priority': 134},
            'DVP27M30F_LT_Calc': {'SWBin': 97, 'HWBin': 5, 'Priority': 135},
            'PLCK_Freq': {'SWBin': 93, 'HWBin': 5, 'Priority': 136},
            'LT_DRow_R': {'SWBin': 25, 'HWBin': 4, 'Priority': 137, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_DRow_Gr': {'SWBin': 25, 'HWBin': 4, 'Priority': 138, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_DRow_Gb': {'SWBin': 25, 'HWBin': 4, 'Priority': 139, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_DRow_B': {'SWBin': 25, 'HWBin': 4, 'Priority': 140, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_DCol_R': {'SWBin': 24, 'HWBin': 4, 'Priority': 141, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_DCol_Gr': {'SWBin': 24, 'HWBin': 4, 'Priority': 142, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_DCol_Gb': {'SWBin': 24, 'HWBin': 4, 'Priority': 143, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_DCol_B': {'SWBin': 24, 'HWBin': 4, 'Priority': 144, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_DRow_Color': {'SWBin': 25, 'HWBin': 4, 'Priority': 145, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_DCol_Color': {'SWBin': 24, 'HWBin': 4, 'Priority': 146, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_WeakLineRow_R': {'SWBin': 25, 'HWBin': 4, 'Priority': 147, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_WeakLineRow_Gr': {'SWBin': 25, 'HWBin': 4, 'Priority': 148, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_WeakLineRow_Gb': {'SWBin': 25, 'HWBin': 4, 'Priority': 149, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_WeakLineRow_B': {'SWBin': 25, 'HWBin': 4, 'Priority': 150, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_WeakLineCol_R': {'SWBin': 24, 'HWBin': 4, 'Priority': 151, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_WeakLineCol_Gr': {'SWBin': 24, 'HWBin': 4, 'Priority': 152, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_WeakLineCol_Gb': {'SWBin': 24, 'HWBin': 4, 'Priority': 153, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_WeakLineCol_B': {'SWBin': 24, 'HWBin': 4, 'Priority': 154, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_Mean_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 155, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_Mean_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 156, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_Mean_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 157, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_Mean_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 158, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_StdDEV_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 159, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_StdDEV_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 160, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_StdDEV_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 161, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_StdDEV_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 162, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_RI_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 163, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_RI_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 164, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_RI_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 165, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_RI_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 166, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_Ratio_GrR': {'SWBin': 23, 'HWBin': 4, 'Priority': 167, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_Ratio_GbR': {'SWBin': 23, 'HWBin': 4, 'Priority': 168, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_Ratio_GrB': {'SWBin': 23, 'HWBin': 4, 'Priority': 169, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_Ratio_GbB': {'SWBin': 23, 'HWBin': 4, 'Priority': 170, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_Ratio_GbGr': {'SWBin': 23, 'HWBin': 4, 'Priority': 171, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_LostBit': {'SWBin': 23, 'HWBin': 4, 'Priority': 172, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_LostBitSNR_SumDIFF_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 173, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_LostBitSNR_SumDIFF_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 174, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_LostBitSNR_SumDIFF_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 175, 'IsNan': 'DVP27M30F_LT_Cap'},
            'LT_LostBitSNR_SumDIFF_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 176, 'IsNan': 'DVP27M30F_LT_Cap'},
            'DVP27M30F_LBIT_Cap': {'SWBin': 99, 'HWBin': 5, 'Priority': 177},
            'DVP27M30F_LBIT_Calc': {'SWBin': 97, 'HWBin': 5, 'Priority': 178},
            'LBIT_LT_Mean_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 179, 'IsNan': 'DVP27M30F_LBIT_Cap'},
            'LBIT_LT_Mean_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 180, 'IsNan': 'DVP27M30F_LBIT_Cap'},
            'LBIT_LT_Mean_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 181, 'IsNan': 'DVP27M30F_LBIT_Cap'},
            'LBIT_LT_Mean_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 182, 'IsNan': 'DVP27M30F_LBIT_Cap'},
            'LBIT_LT_LostBit': {'SWBin': 23, 'HWBin': 4, 'Priority': 183, 'IsNan': 'DVP27M30F_LBIT_Cap'},
            'LBIT_LT_LostBitSNR_SumDIFF_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 184, 'IsNan': 'DVP27M30F_LBIT_Cap'},
            'LBIT_LT_LostBitSNR_SumDIFF_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 185, 'IsNan': 'DVP27M30F_LBIT_Cap'},
            'LBIT_LT_LostBitSNR_SumDIFF_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 186, 'IsNan': 'DVP27M30F_LBIT_Cap'},
            'LBIT_LT_LostBitSNR_SumDIFF_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 187, 'IsNan': 'DVP27M30F_LBIT_Cap'},
            'DVP27M30F_FW_Cap': {'SWBin': 99, 'HWBin': 5, 'Priority': 188},
            'DVP27M30F_FW_Calc': {'SWBin': 97, 'HWBin': 5, 'Priority': 189},
            'FW_LT_DRow_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 190, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_DRow_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 191, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_DRow_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 192, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_DRow_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 193, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_DCol_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 194, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_DCol_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 195, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_DCol_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 196, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_DCol_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 197, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_DRow_Color': {'SWBin': 36, 'HWBin': 4, 'Priority': 198, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_DCol_Color': {'SWBin': 36, 'HWBin': 4, 'Priority': 199, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_Mean_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 200, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_Mean_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 201, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_Mean_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 202, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_Mean_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 203, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_StdDEV_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 204, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_StdDEV_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 205, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_StdDEV_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 206, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_StdDEV_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 207, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_RI_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 208, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_RI_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 209, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_RI_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 210, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_RI_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 211, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_Ratio_GrR': {'SWBin': 36, 'HWBin': 4, 'Priority': 212, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_Ratio_GbR': {'SWBin': 36, 'HWBin': 4, 'Priority': 213, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_Ratio_GrB': {'SWBin': 36, 'HWBin': 4, 'Priority': 214, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_Ratio_GbB': {'SWBin': 36, 'HWBin': 4, 'Priority': 215, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_Ratio_GbGr': {'SWBin': 36, 'HWBin': 4, 'Priority': 216, 'IsNan': 'DVP27M30F_FW_Cap'},
            'FW_LT_LostBit': {'SWBin': 36, 'HWBin': 4, 'Priority': 217, 'IsNan': 'DVP27M30F_FW_Cap'},
            'DVP27M30F_BSun_Cap': {'SWBin': 96, 'HWBin': 5, 'Priority': 218},
            'DVP27M30F_BSun_Calc': {'SWBin': 97, 'HWBin': 5, 'Priority': 219},
            'BSun_BK_DeadRowExBPix_R': {'SWBin': 48, 'HWBin': 6, 'Priority': 220, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_DeadRowExBPix_Gr': {'SWBin': 48, 'HWBin': 6, 'Priority': 221, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_DeadRowExBPix_Gb': {'SWBin': 48, 'HWBin': 6, 'Priority': 222, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_DeadRowExBPix_B': {'SWBin': 48, 'HWBin': 6, 'Priority': 223, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_DeadColExBPix_R': {'SWBin': 47, 'HWBin': 6, 'Priority': 224, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_DeadColExBPix_Gr': {'SWBin': 47, 'HWBin': 6, 'Priority': 225, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_DeadColExBPix_Gb': {'SWBin': 47, 'HWBin': 6, 'Priority': 226, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_DeadColExBPix_B': {'SWBin': 47, 'HWBin': 6, 'Priority': 227, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_Mean_R': {'SWBin': 46, 'HWBin': 6, 'Priority': 228, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_Mean_Gr': {'SWBin': 46, 'HWBin': 6, 'Priority': 229, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_Mean_Gb': {'SWBin': 46, 'HWBin': 6, 'Priority': 230, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_Mean_B': {'SWBin': 46, 'HWBin': 6, 'Priority': 231, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_StdDEV_R': {'SWBin': 46, 'HWBin': 6, 'Priority': 232, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_StdDEV_Gr': {'SWBin': 46, 'HWBin': 6, 'Priority': 233, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_StdDEV_Gb': {'SWBin': 46, 'HWBin': 6, 'Priority': 234, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'BSun_BK_StdDEV_B': {'SWBin': 46, 'HWBin': 6, 'Priority': 235, 'IsNan': 'DVP27M30F_BSun_Cap'},
            'DVP27M30F_LMFlip_Cap': {'SWBin': 96, 'HWBin': 5, 'Priority': 236},
            'DVP27M30F_LMFlip_Calc': {'SWBin': 97, 'HWBin': 5, 'Priority': 237},
            'LMFlip_LT_DRow_R': {'SWBin': 58, 'HWBin': 4, 'Priority': 238, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_DRow_Gr': {'SWBin': 58, 'HWBin': 4, 'Priority': 239, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_DRow_Gb': {'SWBin': 58, 'HWBin': 4, 'Priority': 240, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_DRow_B': {'SWBin': 58, 'HWBin': 4, 'Priority': 241, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_DCol_R': {'SWBin': 57, 'HWBin': 4, 'Priority': 242, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_DCol_Gr': {'SWBin': 57, 'HWBin': 4, 'Priority': 243, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_DCol_Gb': {'SWBin': 57, 'HWBin': 4, 'Priority': 244, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_DCol_B': {'SWBin': 57, 'HWBin': 4, 'Priority': 245, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_DRow_Color': {'SWBin': 58, 'HWBin': 4, 'Priority': 246, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_DCol_Color': {'SWBin': 57, 'HWBin': 4, 'Priority': 247, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_WeakLineRow_R': {'SWBin': 58, 'HWBin': 4, 'Priority': 248, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_WeakLineRow_Gr': {'SWBin': 58, 'HWBin': 4, 'Priority': 249, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_WeakLineRow_Gb': {'SWBin': 58, 'HWBin': 4, 'Priority': 250, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_WeakLineRow_B': {'SWBin': 58, 'HWBin': 4, 'Priority': 251, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_WeakLineCol_R': {'SWBin': 57, 'HWBin': 4, 'Priority': 252, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_WeakLineCol_Gr': {'SWBin': 57, 'HWBin': 4, 'Priority': 253, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_WeakLineCol_Gb': {'SWBin': 57, 'HWBin': 4, 'Priority': 254, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_WeakLineCol_B': {'SWBin': 57, 'HWBin': 4, 'Priority': 255, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_Mean_R': {'SWBin': 56, 'HWBin': 4, 'Priority': 256, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_Mean_Gr': {'SWBin': 56, 'HWBin': 4, 'Priority': 257, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_Mean_Gb': {'SWBin': 56, 'HWBin': 4, 'Priority': 258, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_Mean_B': {'SWBin': 56, 'HWBin': 4, 'Priority': 259, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_StdDEV_R': {'SWBin': 56, 'HWBin': 4, 'Priority': 260, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_StdDEV_Gr': {'SWBin': 56, 'HWBin': 4, 'Priority': 261, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_StdDEV_Gb': {'SWBin': 56, 'HWBin': 4, 'Priority': 262, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_StdDEV_B': {'SWBin': 56, 'HWBin': 4, 'Priority': 263, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_RI_R': {'SWBin': 56, 'HWBin': 4, 'Priority': 264, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_RI_Gr': {'SWBin': 56, 'HWBin': 4, 'Priority': 265, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_RI_Gb': {'SWBin': 56, 'HWBin': 4, 'Priority': 266, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_RI_B': {'SWBin': 56, 'HWBin': 4, 'Priority': 267, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_Ratio_GrR': {'SWBin': 56, 'HWBin': 4, 'Priority': 268, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_Ratio_GbR': {'SWBin': 56, 'HWBin': 4, 'Priority': 269, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_Ratio_GrB': {'SWBin': 56, 'HWBin': 4, 'Priority': 270, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_Ratio_GbB': {'SWBin': 56, 'HWBin': 4, 'Priority': 271, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_Ratio_GbGr': {'SWBin': 56, 'HWBin': 4, 'Priority': 272, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_LostBit': {'SWBin': 56, 'HWBin': 4, 'Priority': 273, 'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_LostBitSNR_SumDIFF_R': {'SWBin': 56, 'HWBin': 4, 'Priority': 274,
                                               'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_LostBitSNR_SumDIFF_Gr': {'SWBin': 56, 'HWBin': 4, 'Priority': 275,
                                                'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_LostBitSNR_SumDIFF_Gb': {'SWBin': 56, 'HWBin': 4, 'Priority': 276,
                                                'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LMFlip_LT_LostBitSNR_SumDIFF_B': {'SWBin': 56, 'HWBin': 4, 'Priority': 277,
                                               'IsNan': 'DVP27M30F_LMFlip_Cap'},
            'LT_CornerLine': {'SWBin': 26, 'HWBin': 4, 'Priority': 278},
            'LT_ScratchLine': {'SWBin': 26, 'HWBin': 4, 'Priority': 279},
            'LT_Blemish': {'SWBin': 31, 'HWBin': 4, 'Priority': 280},
            'LT_LineStripe': {'SWBin': 27, 'HWBin': 4, 'Priority': 281},
            'LT_Particle': {'SWBin': 32, 'HWBin': 4, 'Priority': 282},
            'BK_Cluster2': {'SWBin': 30, 'HWBin': 4, 'Priority': 283},  # 4/8
            'LT_Cluster2': {'SWBin': 30, 'HWBin': 4, 'Priority': 284},  # 4/8
            'BK_Cluster1': {'SWBin': 29, 'HWBin': 4, 'Priority': 285},  # 4/8
            'LT_Cluster1': {'SWBin': 29, 'HWBin': 4, 'Priority': 286},  # 4/8
            'BK_Cluster3GrGb': {'SWBin': 39, 'HWBin': 4, 'Priority': 287},  # 4/8
            'LT_Cluster3GrGb': {'SWBin': 40, 'HWBin': 4, 'Priority': 288},  # 4/8
            'BK_Cluster3SubtractGrGb': {'SWBin': 33, 'HWBin': 4, 'Priority': 289},  # 4/8
            'LT_Cluster3SubtractGrGb': {'SWBin': 34, 'HWBin': 4, 'Priority': 290},  # 4/8
            'WP_Count': {'SWBin': 35, 'HWBin': 4, 'Priority': 291},  # 6/8
            'BK_Z1_BT_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 292},
            'BK_Z1_BT_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 293},
            'BK_Z1_BT_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 294},
            'BK_Z1_BT_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 295},
            'BK_Z2_BT_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 296},
            'BK_Z2_BT_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 297},
            'BK_Z2_BT_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 298},
            'BK_Z2_BT_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 299},
            'BK_Z1_BT_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 300},
            'BK_Z1_BT_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 301},
            'BK_Z1_BT_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 302},
            'BK_Z1_BT_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 303},
            'BK_Z2_BT_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 304},
            'BK_Z2_BT_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 305},
            'BK_Z2_BT_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 306},
            'BK_Z2_BT_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 307},
            'LT_Z1_BT_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 308},
            'LT_Z1_BT_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 309},
            'LT_Z1_BT_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 310},
            'LT_Z1_BT_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 311},
            'LT_Z2_BT_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 312},
            'LT_Z2_BT_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 313},
            'LT_Z2_BT_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 314},
            'LT_Z2_BT_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 315},
            'LT_Z1_BT_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 316},
            'LT_Z1_BT_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 317},
            'LT_Z1_BT_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 318},
            'LT_Z1_BT_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 319},
            'LT_Z2_BT_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 320},
            'LT_Z2_BT_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 321},
            'LT_Z2_BT_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 322},
            'LT_Z2_BT_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 323},
            'LT_Z1_DK_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 324},
            'LT_Z1_DK_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 325},
            'LT_Z1_DK_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 326},
            'LT_Z1_DK_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 327},
            'LT_Z2_DK_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 328},
            'LT_Z2_DK_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 329},
            'LT_Z2_DK_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 330},
            'LT_Z2_DK_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 331},
            'LT_Z1_DK_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 332},
            'LT_Z1_DK_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 333},
            'LT_Z1_DK_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 334},
            'LT_Z1_DK_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 335},
            'LT_Z2_DK_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 336},
            'LT_Z2_DK_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 337},
            'LT_Z2_DK_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 338},
            'LT_Z2_DK_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 339},
            'BK_Z1_BT_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 340},
            'BK_Z2_BT_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 341},
            'BK_Z1_BT_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 342},
            'BK_Z2_BT_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 343},
            'LT_Z1_BT_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 344},
            'LT_Z2_BT_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 345},
            'LT_Z1_BT_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 346},
            'LT_Z2_BT_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 347},
            'LT_Z1_DK_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 348},
            'LT_Z2_DK_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 349},
            'LT_Z1_DK_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 350},
            'LT_Z2_DK_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 351},
            'DVP27M30F_BK32X_Cap': {'SWBin': 98, 'HWBin': 5, 'Priority': 352},
            'DVP27M30F_BK32X_Calc': {'SWBin': 97, 'HWBin': 5, 'Priority': 353},
            'BK32X_BK_BadPixel_Area': {'SWBin': 75, 'HWBin': 4, 'Priority': 354, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DashQty_R': {'SWBin': 51, 'HWBin': 6, 'Priority': 355, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DashQty_Gr': {'SWBin': 51, 'HWBin': 6, 'Priority': 356, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DashQty_Gb': {'SWBin': 51, 'HWBin': 6, 'Priority': 357, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DashQty_B': {'SWBin': 51, 'HWBin': 6, 'Priority': 358, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_SP_BK_MixDCol_DashQty_R': {'SWBin': 54, 'HWBin': 2, 'Priority': 359, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_SP_BK_MixDCol_DashQty_Gr': {'SWBin': 54, 'HWBin': 2, 'Priority': 360,
                                               'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_SP_BK_MixDCol_DashQty_Gb': {'SWBin': 54, 'HWBin': 2, 'Priority': 361,
                                               'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_SP_BK_MixDCol_DashQty_B': {'SWBin': 54, 'HWBin': 2, 'Priority': 362, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_DeltaAvg_R': {'SWBin': 54, 'HWBin': 2, 'Priority': 363,
                                                 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_DeltaAvg_Gr': {'SWBin': 54, 'HWBin': 2, 'Priority': 364,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_DeltaAvg_Gb': {'SWBin': 54, 'HWBin': 2, 'Priority': 365,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_DeltaAvg_B': {'SWBin': 54, 'HWBin': 2, 'Priority': 366,
                                                 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue0_R': {'SWBin': 54, 'HWBin': 2, 'Priority': 367,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue0_Gr': {'SWBin': 54, 'HWBin': 2, 'Priority': 368,
                                                   'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue0_Gb': {'SWBin': 54, 'HWBin': 2, 'Priority': 369,
                                                   'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue0_B': {'SWBin': 54, 'HWBin': 2, 'Priority': 370,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue1_R': {'SWBin': 54, 'HWBin': 2, 'Priority': 371,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue1_Gr': {'SWBin': 54, 'HWBin': 2, 'Priority': 372,
                                                   'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue1_Gb': {'SWBin': 54, 'HWBin': 2, 'Priority': 373,
                                                   'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue1_B': {'SWBin': 54, 'HWBin': 2, 'Priority': 374,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue2_R': {'SWBin': 54, 'HWBin': 2, 'Priority': 375,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue2_Gr': {'SWBin': 54, 'HWBin': 2, 'Priority': 376,
                                                   'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue2_Gb': {'SWBin': 54, 'HWBin': 2, 'Priority': 377,
                                                   'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue2_B': {'SWBin': 54, 'HWBin': 2, 'Priority': 378,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue3_R': {'SWBin': 54, 'HWBin': 2, 'Priority': 379,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue3_Gr': {'SWBin': 54, 'HWBin': 2, 'Priority': 380,
                                                   'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue3_Gb': {'SWBin': 54, 'HWBin': 2, 'Priority': 381,
                                                   'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue3_B': {'SWBin': 54, 'HWBin': 2, 'Priority': 382,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue4_R': {'SWBin': 54, 'HWBin': 2, 'Priority': 383,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue4_Gr': {'SWBin': 54, 'HWBin': 2, 'Priority': 384,
                                                   'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue4_Gb': {'SWBin': 54, 'HWBin': 2, 'Priority': 385,
                                                   'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue4_B': {'SWBin': 54, 'HWBin': 2, 'Priority': 386,
                                                  'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_Mean_R': {'SWBin': 53, 'HWBin': 2, 'Priority': 387, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_Mean_Gr': {'SWBin': 53, 'HWBin': 2, 'Priority': 388, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_Mean_Gb': {'SWBin': 53, 'HWBin': 2, 'Priority': 389, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_Mean_B': {'SWBin': 53, 'HWBin': 2, 'Priority': 390, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_StdDEV_R': {'SWBin': 53, 'HWBin': 2, 'Priority': 391, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_StdDEV_Gr': {'SWBin': 53, 'HWBin': 2, 'Priority': 392, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_StdDEV_Gb': {'SWBin': 53, 'HWBin': 2, 'Priority': 393, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK32X_BK_StdDEV_B': {'SWBin': 53, 'HWBin': 2, 'Priority': 394, 'IsNan': 'DVP27M30F_BK32X_Cap'},
            'BK_Cluster3_2': {'SWBin': 73, 'HWBin': 2, 'Priority': 395},
            'LT_Cluster3_2': {'SWBin': 74, 'HWBin': 2, 'Priority': 396},
            'MIPI2L24M30F_WK1_Cap': {'SWBin': 89, 'HWBin': 1, 'Priority': 397},
            'MIPI2L24M30F_WK1_Calc': {'SWBin': 97, 'HWBin': 5, 'Priority': 398},
            'MIPI_One_W1_FixedPattern': {'SWBin': 94, 'HWBin': 1, 'Priority': 399, 'IsNan': 'MIPI2L24M30F_WK1_Cap'},
            'MIPI2L24M30F_LT_Cap': {'SWBin': 90, 'HWBin': 1, 'Priority': 400},
            'MIPI2L24M30F_LT_Calc': {'SWBin': 97, 'HWBin': 5, 'Priority': 401},
            'MIPI_LT_DRow_R': {'SWBin': 65, 'HWBin': 1, 'Priority': 402, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_DRow_Gr': {'SWBin': 65, 'HWBin': 1, 'Priority': 403, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_DRow_Gb': {'SWBin': 65, 'HWBin': 1, 'Priority': 404, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_DRow_B': {'SWBin': 65, 'HWBin': 1, 'Priority': 405, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_DCol_R': {'SWBin': 64, 'HWBin': 1, 'Priority': 406, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_DCol_Gr': {'SWBin': 64, 'HWBin': 1, 'Priority': 407, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_DCol_Gb': {'SWBin': 64, 'HWBin': 1, 'Priority': 408, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_DCol_B': {'SWBin': 64, 'HWBin': 1, 'Priority': 409, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_DRow_Color': {'SWBin': 65, 'HWBin': 1, 'Priority': 410, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_DCol_Color': {'SWBin': 64, 'HWBin': 1, 'Priority': 411, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_WeakLineRow_R': {'SWBin': 65, 'HWBin': 1, 'Priority': 412, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_WeakLineRow_Gr': {'SWBin': 65, 'HWBin': 1, 'Priority': 413, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_WeakLineRow_Gb': {'SWBin': 65, 'HWBin': 1, 'Priority': 414, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_WeakLineRow_B': {'SWBin': 65, 'HWBin': 1, 'Priority': 415, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_WeakLineCol_R': {'SWBin': 64, 'HWBin': 1, 'Priority': 416, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_WeakLineCol_Gr': {'SWBin': 64, 'HWBin': 1, 'Priority': 417, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_WeakLineCol_Gb': {'SWBin': 64, 'HWBin': 1, 'Priority': 418, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_WeakLineCol_B': {'SWBin': 64, 'HWBin': 1, 'Priority': 419, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_Mean_R': {'SWBin': 63, 'HWBin': 1, 'Priority': 420, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_Mean_Gr': {'SWBin': 63, 'HWBin': 1, 'Priority': 421, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_Mean_Gb': {'SWBin': 63, 'HWBin': 1, 'Priority': 422, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_Mean_B': {'SWBin': 63, 'HWBin': 1, 'Priority': 423, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_StdDEV_R': {'SWBin': 63, 'HWBin': 1, 'Priority': 424, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_StdDEV_Gr': {'SWBin': 63, 'HWBin': 1, 'Priority': 425, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_StdDEV_Gb': {'SWBin': 63, 'HWBin': 1, 'Priority': 426, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_StdDEV_B': {'SWBin': 63, 'HWBin': 1, 'Priority': 427, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_RI_R': {'SWBin': 63, 'HWBin': 1, 'Priority': 428, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_RI_Gr': {'SWBin': 63, 'HWBin': 1, 'Priority': 429, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_RI_Gb': {'SWBin': 63, 'HWBin': 1, 'Priority': 430, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_RI_B': {'SWBin': 63, 'HWBin': 1, 'Priority': 431, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_Ratio_GrR': {'SWBin': 63, 'HWBin': 1, 'Priority': 432, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_Ratio_GbR': {'SWBin': 63, 'HWBin': 1, 'Priority': 433, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_Ratio_GrB': {'SWBin': 63, 'HWBin': 1, 'Priority': 434, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_Ratio_GbB': {'SWBin': 63, 'HWBin': 1, 'Priority': 435, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_Ratio_GbGr': {'SWBin': 63, 'HWBin': 1, 'Priority': 436, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_LostBit': {'SWBin': 63, 'HWBin': 1, 'Priority': 437, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_LostBitSNR_SumDIFF_R': {'SWBin': 63, 'HWBin': 1, 'Priority': 438, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_LostBitSNR_SumDIFF_Gr': {'SWBin': 63, 'HWBin': 1, 'Priority': 439, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_LostBitSNR_SumDIFF_Gb': {'SWBin': 63, 'HWBin': 1, 'Priority': 440, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI_LT_LostBitSNR_SumDIFF_B': {'SWBin': 63, 'HWBin': 1, 'Priority': 441, 'IsNan': 'MIPI2L24M30F_LT_Cap'},
            'MIPI2L24M30F_LBIT_Cap': {'SWBin': 90, 'HWBin': 1, 'Priority': 442},
            'MIPI2L24M30F_LBIT_Calc': {'SWBin': 97, 'HWBin': 5, 'Priority': 443},
            'MIPI_LBIT_LT_Mean_R': {'SWBin': 63, 'HWBin': 1, 'Priority': 444, 'IsNan': 'MIPI2L24M30F_LBIT_Cap'},
            'MIPI_LBIT_LT_Mean_Gr': {'SWBin': 63, 'HWBin': 1, 'Priority': 445, 'IsNan': 'MIPI2L24M30F_LBIT_Cap'},
            'MIPI_LBIT_LT_Mean_Gb': {'SWBin': 63, 'HWBin': 1, 'Priority': 446, 'IsNan': 'MIPI2L24M30F_LBIT_Cap'},
            'MIPI_LBIT_LT_Mean_B': {'SWBin': 63, 'HWBin': 1, 'Priority': 447, 'IsNan': 'MIPI2L24M30F_LBIT_Cap'},
            'MIPI_LBIT_LT_LostBit': {'SWBin': 63, 'HWBin': 1, 'Priority': 448, 'IsNan': 'MIPI2L24M30F_LBIT_Cap'},
            'MIPI_LBIT_LT_LostBitSNR_SumDIFF_R': {'SWBin': 63, 'HWBin': 1, 'Priority': 449,
                                                  'IsNan': 'MIPI2L24M30F_LBIT_Cap'},
            'MIPI_LBIT_LT_LostBitSNR_SumDIFF_Gr': {'SWBin': 63, 'HWBin': 1, 'Priority': 450,
                                                   'IsNan': 'MIPI2L24M30F_LBIT_Cap'},
            'MIPI_LBIT_LT_LostBitSNR_SumDIFF_Gb': {'SWBin': 63, 'HWBin': 1, 'Priority': 451,
                                                   'IsNan': 'MIPI2L24M30F_LBIT_Cap'},
            'MIPI_LBIT_LT_LostBitSNR_SumDIFF_B': {'SWBin': 63, 'HWBin': 1, 'Priority': 452,
                                                  'IsNan': 'MIPI2L24M30F_LBIT_Cap'},
            'Binning': {'SWBin': 2, 'HWBin': 3, 'Priority': 453},
            'All Pass': {'SWBin': 1, 'HWBin': 3, 'Priority': 454}
        },
    'JX825':
        {
            'VSYNC_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 1},
            'HSYNC_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 2},
            'PCLK_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 3},
            'EXCLK_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 4},
            'RSTB_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 5},
            'PWDN_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 6},
            'SDA_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 7},
            'SCL_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 8},
            'VH_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 9},
            'VN1_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 10},
            'VN2_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 11},
            'D0_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 12},
            'D1_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 13},
            'D2_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 14},
            'D3_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 15},
            'D4_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 16},
            'D5_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 17},
            'D6_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 18},
            'D7_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 19},
            'D8_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 20},
            'D9_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 21},
            'MCP_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 22},
            'MCN_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 23},
            'MDP0_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 24},
            'MDN0_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 25},
            'MDP1_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 26},
            'MDN1_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 27},
            'MDP2_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 28},
            'MDN2_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 29},
            'MDP3_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 30},
            'MDN3_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 31},
            'DVDD_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 32},
            'AVDD_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 33},
            'DOVDD_O/S': {'SWBin': 5, 'HWBin': 5, 'Priority': 34},
            'VSYNC_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 35},
            'HSYNC_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 36},
            'PCLK_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 37},
            'EXCLK_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 38},
            'RSTB_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 39},
            'PWDN_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 40},
            'SDA_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 41},
            'SCL_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 42},
            'D0_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 43},
            'D1_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 44},
            'D2_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 45},
            'D3_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 46},
            'D4_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 47},
            'D5_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 48},
            'D6_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 49},
            'D7_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 50},
            'D8_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 51},
            'D9_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 52},
            'MCP_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 53},
            'MCN_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 54},
            'MDP0_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 55},
            'MDN0_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 56},
            'MDP1_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 57},
            'MDN1_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 58},
            'MDP2_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 59},
            'MDN2_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 60},
            'MDP3_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 61},
            'MDN3_Leakage/iiL': {'SWBin': 6, 'HWBin': 5, 'Priority': 62},
            'VSYNC_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 63},
            'HSYNC_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 64},
            'PCLK_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 65},
            'EXCLK_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 66},
            'RSTB_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 67},
            'PWDN_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 68},
            'SDA_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 69},
            'SCL_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 70},
            'D0_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 71},
            'D1_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 72},
            'D2_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 73},
            'D3_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 74},
            'D4_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 75},
            'D5_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 76},
            'D6_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 77},
            'D7_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 78},
            'D8_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 79},
            'D9_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 80},
            'MCP_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 81},
            'MCN_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 82},
            'MDP0_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 83},
            'MDN0_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 84},
            'MDP1_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 85},
            'MDN1_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 86},
            'MDP2_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 87},
            'MDN2_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 88},
            'MDP3_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 89},
            'MDN3_Leakage/iiH': {'SWBin': 6, 'HWBin': 5, 'Priority': 90},
            'iic_test': {'SWBin': 7, 'HWBin': 5, 'Priority': 91},
            'MIPI4L27M30F_BK_Cap': {'SWBin': 98, 'HWBin': 8, 'Priority': 92},
            'MIPI4L27M30F_BK_Calc': {'SWBin': 97, 'HWBin': 8, 'Priority': 93},
            'BLC_R': {'SWBin': 7, 'HWBin': 5, 'Priority': 94},
            'BLC_Gr': {'SWBin': 7, 'HWBin': 5, 'Priority': 95},
            'BLC_Gb': {'SWBin': 7, 'HWBin': 5, 'Priority': 96},
            'BLC_B': {'SWBin': 7, 'HWBin': 5, 'Priority': 97},
            'BK_DeadRowExBPix_R': {'SWBin': 15, 'HWBin': 6, 'Priority': 98, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_DeadRowExBPix_Gr': {'SWBin': 15, 'HWBin': 6, 'Priority': 99, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_DeadRowExBPix_Gb': {'SWBin': 15, 'HWBin': 6, 'Priority': 100, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_DeadRowExBPix_B': {'SWBin': 15, 'HWBin': 6, 'Priority': 101, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_DeadColExBPix_R': {'SWBin': 14, 'HWBin': 6, 'Priority': 102, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_DeadColExBPix_Gr': {'SWBin': 14, 'HWBin': 6, 'Priority': 103, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_DeadColExBPix_Gb': {'SWBin': 14, 'HWBin': 6, 'Priority': 104, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_DeadColExBPix_B': {'SWBin': 14, 'HWBin': 6, 'Priority': 105, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VfpnQty_R': {'SWBin': 14, 'HWBin': 6, 'Priority': 106, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VfpnQty_Gr': {'SWBin': 14, 'HWBin': 6, 'Priority': 107, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VfpnQty_Gb': {'SWBin': 14, 'HWBin': 6, 'Priority': 108, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VfpnQty_B': {'SWBin': 14, 'HWBin': 6, 'Priority': 109, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue0_R': {'SWBin': 13, 'HWBin': 6, 'Priority': 110, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue0_Gr': {'SWBin': 13, 'HWBin': 6, 'Priority': 111, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue0_Gb': {'SWBin': 13, 'HWBin': 6, 'Priority': 112, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue0_B': {'SWBin': 13, 'HWBin': 6, 'Priority': 113, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue1_R': {'SWBin': 13, 'HWBin': 6, 'Priority': 114, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue1_Gr': {'SWBin': 13, 'HWBin': 6, 'Priority': 115, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue1_Gb': {'SWBin': 13, 'HWBin': 6, 'Priority': 116, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue1_B': {'SWBin': 13, 'HWBin': 6, 'Priority': 117, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue2_R': {'SWBin': 13, 'HWBin': 6, 'Priority': 118, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue2_Gr': {'SWBin': 13, 'HWBin': 6, 'Priority': 119, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue2_Gb': {'SWBin': 13, 'HWBin': 6, 'Priority': 120, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue2_B': {'SWBin': 13, 'HWBin': 6, 'Priority': 121, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue3_R': {'SWBin': 13, 'HWBin': 6, 'Priority': 122, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue3_Gr': {'SWBin': 13, 'HWBin': 6, 'Priority': 123, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue3_Gb': {'SWBin': 13, 'HWBin': 6, 'Priority': 124, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue3_B': {'SWBin': 13, 'HWBin': 6, 'Priority': 125, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue4_R': {'SWBin': 13, 'HWBin': 6, 'Priority': 126, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue4_Gr': {'SWBin': 13, 'HWBin': 6, 'Priority': 127, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue4_Gb': {'SWBin': 13, 'HWBin': 6, 'Priority': 128, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_MixDCol_VFPN_MaxValue4_B': {'SWBin': 13, 'HWBin': 6, 'Priority': 129, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_Mean_R': {'SWBin': 13, 'HWBin': 6, 'Priority': 130, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_Mean_Gr': {'SWBin': 13, 'HWBin': 6, 'Priority': 131, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_Mean_Gb': {'SWBin': 13, 'HWBin': 6, 'Priority': 132, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_Mean_B': {'SWBin': 13, 'HWBin': 6, 'Priority': 133, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_StdDEV_R': {'SWBin': 13, 'HWBin': 6, 'Priority': 134, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_StdDEV_Gr': {'SWBin': 13, 'HWBin': 6, 'Priority': 135, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_StdDEV_Gb': {'SWBin': 13, 'HWBin': 6, 'Priority': 136, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'BK_StdDEV_B': {'SWBin': 13, 'HWBin': 6, 'Priority': 137, 'IsNan': 'MIPI4L27M30F_BK_Cap'},
            'VH_voltage': {'SWBin': 9, 'HWBin': 5, 'Priority': 138},
            'VN1_voltage': {'SWBin': 9, 'HWBin': 5, 'Priority': 139},
            'VN2_voltage': {'SWBin': 9, 'HWBin': 5, 'Priority': 140},
            'DVDD_voltage': {'SWBin': 9, 'HWBin': 5, 'Priority': 141},
            'MIPI4L27M30F_LT_Cap': {'SWBin': 99, 'HWBin': 8, 'Priority': 142},
            'MIPI4L27M30F_LT_Calc': {'SWBin': 99, 'HWBin': 8, 'Priority': 143},
            'LT_DRow_R': {'SWBin': 25, 'HWBin': 4, 'Priority': 144, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_DRow_Gr': {'SWBin': 25, 'HWBin': 4, 'Priority': 145, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_DRow_Gb': {'SWBin': 25, 'HWBin': 4, 'Priority': 146, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_DRow_B': {'SWBin': 25, 'HWBin': 4, 'Priority': 147, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_DCol_R': {'SWBin': 24, 'HWBin': 4, 'Priority': 148, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_DCol_Gr': {'SWBin': 24, 'HWBin': 4, 'Priority': 149, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_DCol_Gb': {'SWBin': 24, 'HWBin': 4, 'Priority': 150, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_DCol_B': {'SWBin': 24, 'HWBin': 4, 'Priority': 151, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_DRow_Color': {'SWBin': 25, 'HWBin': 4, 'Priority': 152, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_DCol_Color': {'SWBin': 24, 'HWBin': 4, 'Priority': 153, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_WeakLineRow_R': {'SWBin': 25, 'HWBin': 4, 'Priority': 154, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_WeakLineRow_Gr': {'SWBin': 25, 'HWBin': 4, 'Priority': 155, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_WeakLineRow_Gb': {'SWBin': 25, 'HWBin': 4, 'Priority': 156, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_WeakLineRow_B': {'SWBin': 25, 'HWBin': 4, 'Priority': 157, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_WeakLineCol_R': {'SWBin': 24, 'HWBin': 4, 'Priority': 158, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_WeakLineCol_Gr': {'SWBin': 24, 'HWBin': 4, 'Priority': 159, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_WeakLineCol_Gb': {'SWBin': 24, 'HWBin': 4, 'Priority': 160, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_WeakLineCol_B': {'SWBin': 24, 'HWBin': 4, 'Priority': 161, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_Mean_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 162, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_Mean_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 163, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_Mean_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 164, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_Mean_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 165, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_StdDEV_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 166, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_StdDEV_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 167, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_StdDEV_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 168, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_StdDEV_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 169, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_RI_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 170, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_RI_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 171, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_RI_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 172, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_RI_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 173, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_Ratio_GrR': {'SWBin': 23, 'HWBin': 4, 'Priority': 174, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_Ratio_GbR': {'SWBin': 23, 'HWBin': 4, 'Priority': 175, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_Ratio_GrB': {'SWBin': 23, 'HWBin': 4, 'Priority': 176, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_Ratio_GbB': {'SWBin': 23, 'HWBin': 4, 'Priority': 177, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_Ratio_GbGr': {'SWBin': 23, 'HWBin': 4, 'Priority': 178, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_LostBit': {'SWBin': 23, 'HWBin': 4, 'Priority': 179, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_LostBitSNR_SumDIFF_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 180, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_LostBitSNR_SumDIFF_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 181, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_LostBitSNR_SumDIFF_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 182, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'LT_LostBitSNR_SumDIFF_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 183, 'IsNan': 'MIPI4L27M30F_LT_Cap'},
            'MIPI4L27M30F_LBIT_Cap': {'SWBin': 99, 'HWBin': 8, 'Priority': 184},
            'MIPI4L27M30F_LBIT_Calc': {'SWBin': 97, 'HWBin': 8, 'Priority': 185},
            'LBIT_LT_Mean_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 186, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_Mean_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 187, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_Mean_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 188, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_Mean_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 189, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_DRow_R': {'SWBin': 25, 'HWBin': 4, 'Priority': 190, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_DRow_Gr': {'SWBin': 25, 'HWBin': 4, 'Priority': 191, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_DRow_Gb': {'SWBin': 25, 'HWBin': 4, 'Priority': 192, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_DRow_B': {'SWBin': 25, 'HWBin': 4, 'Priority': 193, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_DCol_R': {'SWBin': 24, 'HWBin': 4, 'Priority': 194, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_DCol_Gr': {'SWBin': 24, 'HWBin': 4, 'Priority': 195, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_DCol_Gb': {'SWBin': 24, 'HWBin': 4, 'Priority': 196, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_DCol_B': {'SWBin': 24, 'HWBin': 4, 'Priority': 197, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_DRow_Color': {'SWBin': 25, 'HWBin': 4, 'Priority': 198, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_DCol_Color': {'SWBin': 24, 'HWBin': 4, 'Priority': 199, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_WeakLineRow_R': {'SWBin': 25, 'HWBin': 4, 'Priority': 200, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_WeakLineRow_Gr': {'SWBin': 25, 'HWBin': 4, 'Priority': 201, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_WeakLineRow_Gb': {'SWBin': 25, 'HWBin': 4, 'Priority': 202, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_WeakLineRow_B': {'SWBin': 25, 'HWBin': 4, 'Priority': 203, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_WeakLineCol_R': {'SWBin': 24, 'HWBin': 4, 'Priority': 204, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_WeakLineCol_Gr': {'SWBin': 24, 'HWBin': 4, 'Priority': 205, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_WeakLineCol_Gb': {'SWBin': 24, 'HWBin': 4, 'Priority': 206, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_WeakLineCol_B': {'SWBin': 24, 'HWBin': 4, 'Priority': 207, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_Cluster2': {'SWBin': 23, 'HWBin': 4, 'Priority': 208, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_Cluster1': {'SWBin': 23, 'HWBin': 4, 'Priority': 209, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_LostBit': {'SWBin': 23, 'HWBin': 4, 'Priority': 210, 'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_LostBitSNR_SumDIFF_R': {'SWBin': 23, 'HWBin': 4, 'Priority': 211,
                                             'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_LostBitSNR_SumDIFF_Gr': {'SWBin': 23, 'HWBin': 4, 'Priority': 212,
                                              'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_LostBitSNR_SumDIFF_Gb': {'SWBin': 23, 'HWBin': 4, 'Priority': 213,
                                              'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LBIT_LT_LostBitSNR_SumDIFF_B': {'SWBin': 23, 'HWBin': 4, 'Priority': 214,
                                             'IsNan': 'MIPI4L27M30F_LBIT_Cap'},
            'LT_CornerLine': {'SWBin': 26, 'HWBin': 4, 'Priority': 215},
            'LT_ScratchLine': {'SWBin': 26, 'HWBin': 4, 'Priority': 216},
            'LT_Blemish': {'SWBin': 31, 'HWBin': 4, 'Priority': 217},
            'LT_LineStripe': {'SWBin': 27, 'HWBin': 4, 'Priority': 218},
            'LT_Particle': {'SWBin': 32, 'HWBin': 4, 'Priority': 219},
            'BK_Cluster2': {'SWBin': 30, 'HWBin': 4, 'Priority': 220},
            'LT_Cluster2': {'SWBin': 30, 'HWBin': 4, 'Priority': 221},
            'BK_Cluster1': {'SWBin': 29, 'HWBin': 4, 'Priority': 222},
            'LT_Cluster1': {'SWBin': 29, 'HWBin': 4, 'Priority': 223},
            'BK_BadPixel_Area': {'SWBin': 33, 'HWBin': 4, 'Priority': 224},
            'LT_BadPixel_Area': {'SWBin': 34, 'HWBin': 4, 'Priority': 225},
            'WP_Count': {'SWBin': 35, 'HWBin': 6, 'Priority': 226},
            'BK_Z1_BT_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 227},
            'BK_Z1_BT_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 228},
            'BK_Z1_BT_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 229},
            'BK_Z1_BT_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 230},
            'BK_Z2_BT_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 231},
            'BK_Z2_BT_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 232},
            'BK_Z2_BT_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 233},
            'BK_Z2_BT_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 234},
            'BK_Z1_BT_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 235},
            'BK_Z1_BT_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 236},
            'BK_Z1_BT_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 237},
            'BK_Z1_BT_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 238},
            'BK_Z2_BT_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 239},
            'BK_Z2_BT_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 240},
            'BK_Z2_BT_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 241},
            'BK_Z2_BT_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 242},
            'LT_Z1_BT_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 243},
            'LT_Z1_BT_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 244},
            'LT_Z1_BT_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 245},
            'LT_Z1_BT_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 246},
            'LT_Z2_BT_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 247},
            'LT_Z2_BT_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 248},
            'LT_Z2_BT_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 249},
            'LT_Z2_BT_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 250},
            'LT_Z1_BT_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 251},
            'LT_Z1_BT_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 252},
            'LT_Z1_BT_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 253},
            'LT_Z1_BT_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 254},
            'LT_Z2_BT_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 255},
            'LT_Z2_BT_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 256},
            'LT_Z2_BT_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 257},
            'LT_Z2_BT_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 258},
            'LT_Z1_DK_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 259},
            'LT_Z1_DK_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 260},
            'LT_Z1_DK_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 261},
            'LT_Z1_DK_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 262},
            'LT_Z2_DK_WP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 263},
            'LT_Z2_DK_WP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 264},
            'LT_Z2_DK_WP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 265},
            'LT_Z2_DK_WP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 266},
            'LT_Z1_DK_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 267},
            'LT_Z1_DK_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 268},
            'LT_Z1_DK_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 269},
            'LT_Z1_DK_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 270},
            'LT_Z2_DK_DP_R': {'SWBin': 60, 'HWBin': 6, 'Priority': 271},
            'LT_Z2_DK_DP_Gr': {'SWBin': 60, 'HWBin': 6, 'Priority': 272},
            'LT_Z2_DK_DP_Gb': {'SWBin': 60, 'HWBin': 6, 'Priority': 273},
            'LT_Z2_DK_DP_B': {'SWBin': 60, 'HWBin': 6, 'Priority': 274},
            'BK_Z1_BT_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 275},
            'BK_Z2_BT_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 276},
            'BK_Z1_BT_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 277},
            'BK_Z2_BT_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 278},
            'LT_Z1_BT_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 279},
            'LT_Z2_BT_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 280},
            'LT_Z1_BT_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 281},
            'LT_Z2_BT_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 282},
            'LT_Z1_DK_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 283},
            'LT_Z2_DK_DP': {'SWBin': 60, 'HWBin': 6, 'Priority': 284},
            'LT_Z1_DK_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 285},
            'LT_Z2_DK_WP': {'SWBin': 60, 'HWBin': 6, 'Priority': 286},
            'Active_AVDD': {'SWBin': 12, 'HWBin': 5, 'Priority': 287},
            'Active_DOVDD': {'SWBin': 12, 'HWBin': 5, 'Priority': 288},
            'PWDN_AVDD': {'SWBin': 8, 'HWBin': 5, 'Priority': 289},
            'PWDN_DOVDD': {'SWBin': 8, 'HWBin': 5, 'Priority': 290},
            'PWDN_Total': {'SWBin': 8, 'HWBin': 5, 'Priority': 291},
            'BK_Cluster3GrGb': {'SWBin': 39, 'HWBin': 4, 'Priority': 292},
            'LT_Cluster3GrGb': {'SWBin': 40, 'HWBin': 4, 'Priority': 293},
            'MIPI4L27M30F_FW_Cap': {'SWBin': 99, 'HWBin': 8, 'Priority': 294},
            'MIPI4L27M30F_FW_Calc': {'SWBin': 97, 'HWBin': 8, 'Priority': 295},
            'FW_LT_DRow_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 296, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_DRow_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 297, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_DRow_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 298, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_DRow_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 299, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_DCol_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 300, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_DCol_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 301, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_DCol_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 302, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_DCol_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 303, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_DRow_Color': {'SWBin': 36, 'HWBin': 4, 'Priority': 304, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_DCol_Color': {'SWBin': 36, 'HWBin': 4, 'Priority': 305, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_Mean_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 306, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_Mean_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 307, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_Mean_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 308, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_Mean_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 309, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_StdDEV_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 310, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_StdDEV_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 311, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_StdDEV_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 312, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_StdDEV_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 313, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_RI_R': {'SWBin': 36, 'HWBin': 4, 'Priority': 314, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_RI_Gr': {'SWBin': 36, 'HWBin': 4, 'Priority': 315, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_RI_Gb': {'SWBin': 36, 'HWBin': 4, 'Priority': 316, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_RI_B': {'SWBin': 36, 'HWBin': 4, 'Priority': 317, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_Ratio_GrR': {'SWBin': 36, 'HWBin': 4, 'Priority': 318, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_Ratio_GbR': {'SWBin': 36, 'HWBin': 4, 'Priority': 319, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_Ratio_GrB': {'SWBin': 36, 'HWBin': 4, 'Priority': 320, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_Ratio_GbB': {'SWBin': 36, 'HWBin': 4, 'Priority': 321, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_Ratio_GbGr': {'SWBin': 36, 'HWBin': 4, 'Priority': 322, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'FW_LT_LostBit': {'SWBin': 36, 'HWBin': 4, 'Priority': 323, 'IsNan': 'MIPI4L27M30F_FW_Cap'},
            'MIPI2L_LT_Cap': {'SWBin': 90, 'HWBin': 8, 'Priority': 324},
            'MIPI2L_LT_Calc': {'SWBin': 97, 'HWBin': 8, 'Priority': 325},
            'MIPI2L_LT_DRow_R': {'SWBin': 65, 'HWBin': 4, 'Priority': 326, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_DRow_Gr': {'SWBin': 65, 'HWBin': 4, 'Priority': 327, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_DRow_Gb': {'SWBin': 65, 'HWBin': 4, 'Priority': 328, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_DRow_B': {'SWBin': 65, 'HWBin': 4, 'Priority': 329, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_DCol_R': {'SWBin': 64, 'HWBin': 4, 'Priority': 330, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_DCol_Gr': {'SWBin': 64, 'HWBin': 4, 'Priority': 331, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_DCol_Gb': {'SWBin': 64, 'HWBin': 4, 'Priority': 332, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_DCol_B': {'SWBin': 64, 'HWBin': 4, 'Priority': 333, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_DRow_Color': {'SWBin': 65, 'HWBin': 4, 'Priority': 334, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_DCol_Color': {'SWBin': 64, 'HWBin': 4, 'Priority': 335, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_WeakLineRow_R': {'SWBin': 65, 'HWBin': 4, 'Priority': 336, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_WeakLineRow_Gr': {'SWBin': 65, 'HWBin': 4, 'Priority': 337, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_WeakLineRow_Gb': {'SWBin': 65, 'HWBin': 4, 'Priority': 338, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_WeakLineRow_B': {'SWBin': 65, 'HWBin': 4, 'Priority': 339, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_WeakLineCol_R': {'SWBin': 64, 'HWBin': 4, 'Priority': 340, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_WeakLineCol_Gr': {'SWBin': 64, 'HWBin': 4, 'Priority': 341, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_WeakLineCol_Gb': {'SWBin': 64, 'HWBin': 4, 'Priority': 342, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_WeakLineCol_B': {'SWBin': 64, 'HWBin': 4, 'Priority': 343, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_Mean_R': {'SWBin': 63, 'HWBin': 4, 'Priority': 344, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_Mean_Gr': {'SWBin': 63, 'HWBin': 4, 'Priority': 345, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_Mean_Gb': {'SWBin': 63, 'HWBin': 4, 'Priority': 346, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_Mean_B': {'SWBin': 63, 'HWBin': 4, 'Priority': 347, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_StdDEV_R': {'SWBin': 63, 'HWBin': 4, 'Priority': 348, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_StdDEV_Gr': {'SWBin': 63, 'HWBin': 4, 'Priority': 349, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_StdDEV_Gb': {'SWBin': 63, 'HWBin': 4, 'Priority': 350, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_StdDEV_B': {'SWBin': 63, 'HWBin': 4, 'Priority': 351, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_RI_R': {'SWBin': 63, 'HWBin': 4, 'Priority': 352, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_RI_Gr': {'SWBin': 63, 'HWBin': 4, 'Priority': 353, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_RI_Gb': {'SWBin': 63, 'HWBin': 4, 'Priority': 354, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_RI_B': {'SWBin': 63, 'HWBin': 4, 'Priority': 355, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_Ratio_GrR': {'SWBin': 63, 'HWBin': 4, 'Priority': 356, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_Ratio_GbR': {'SWBin': 63, 'HWBin': 4, 'Priority': 357, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_Ratio_GrB': {'SWBin': 63, 'HWBin': 4, 'Priority': 358, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_Ratio_GbB': {'SWBin': 63, 'HWBin': 4, 'Priority': 359, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_Ratio_GbGr': {'SWBin': 63, 'HWBin': 4, 'Priority': 360, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_LostBit': {'SWBin': 63, 'HWBin': 4, 'Priority': 361, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_LostBitSNR_SumDIFF_R': {'SWBin': 63, 'HWBin': 4, 'Priority': 362, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_LostBitSNR_SumDIFF_Gr': {'SWBin': 63, 'HWBin': 4, 'Priority': 363, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_LostBitSNR_SumDIFF_Gb': {'SWBin': 63, 'HWBin': 4, 'Priority': 364, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI2L_LT_LostBitSNR_SumDIFF_B': {'SWBin': 63, 'HWBin': 4, 'Priority': 365, 'IsNan': 'MIPI2L_LT_Cap'},
            'MIPI4L27M30F_BK1X_Cap': {'SWBin': 96, 'HWBin': 8, 'Priority': 366},
            'MIPI4L27M30F_BK1X_Calc': {'SWBin': 97, 'HWBin': 8, 'Priority': 367},
            'BK1X_BK_DeadRowExBPix_R': {'SWBin': 48, 'HWBin': 6, 'Priority': 368, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_DeadRowExBPix_Gr': {'SWBin': 48, 'HWBin': 6, 'Priority': 369, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_DeadRowExBPix_Gb': {'SWBin': 48, 'HWBin': 6, 'Priority': 370, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_DeadRowExBPix_B': {'SWBin': 48, 'HWBin': 6, 'Priority': 371, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_DeadColExBPix_R': {'SWBin': 47, 'HWBin': 6, 'Priority': 372, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_DeadColExBPix_Gr': {'SWBin': 47, 'HWBin': 6, 'Priority': 373, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_DeadColExBPix_Gb': {'SWBin': 47, 'HWBin': 6, 'Priority': 374, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_DeadColExBPix_B': {'SWBin': 47, 'HWBin': 6, 'Priority': 375, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_Mean_R': {'SWBin': 46, 'HWBin': 6, 'Priority': 376, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_Mean_Gr': {'SWBin': 46, 'HWBin': 6, 'Priority': 377, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_Mean_Gb': {'SWBin': 46, 'HWBin': 6, 'Priority': 378, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_Mean_B': {'SWBin': 46, 'HWBin': 6, 'Priority': 379, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_StdDEV_R': {'SWBin': 46, 'HWBin': 6, 'Priority': 380, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_StdDEV_Gr': {'SWBin': 46, 'HWBin': 6, 'Priority': 381, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_StdDEV_Gb': {'SWBin': 46, 'HWBin': 6, 'Priority': 382, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'BK1X_BK_StdDEV_B': {'SWBin': 46, 'HWBin': 6, 'Priority': 383, 'IsNan': 'MIPI4L27M30F_BK1X_Cap'},
            'MIPI4L27M30F_BK32X_Cap': {'SWBin': 96, 'HWBin': 8, 'Priority': 384},
            'MIPI4L27M30F_BK32X_Calc': {'SWBin': 97, 'HWBin': 8, 'Priority': 385},
            'BK32X_BK_MixDCol_DashQty_R': {'SWBin': 54, 'HWBin': 6, 'Priority': 386, 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DashQty_Gr': {'SWBin': 54, 'HWBin': 6, 'Priority': 387,
                                            'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DashQty_Gb': {'SWBin': 54, 'HWBin': 6, 'Priority': 388,
                                            'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DashQty_B': {'SWBin': 54, 'HWBin': 6, 'Priority': 389, 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_DeltaAvg_R': {'SWBin': 54, 'HWBin': 6, 'Priority': 390,
                                                 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_DeltaAvg_Gr': {'SWBin': 54, 'HWBin': 6, 'Priority': 391,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_DeltaAvg_Gb': {'SWBin': 54, 'HWBin': 6, 'Priority': 392,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_DeltaAvg_B': {'SWBin': 54, 'HWBin': 6, 'Priority': 393,
                                                 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue0_R': {'SWBin': 54, 'HWBin': 6, 'Priority': 394,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue0_Gr': {'SWBin': 54, 'HWBin': 6, 'Priority': 395,
                                                   'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue0_Gb': {'SWBin': 54, 'HWBin': 6, 'Priority': 396,
                                                   'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue0_B': {'SWBin': 54, 'HWBin': 6, 'Priority': 397,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue1_R': {'SWBin': 54, 'HWBin': 6, 'Priority': 398,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue1_Gr': {'SWBin': 54, 'HWBin': 6, 'Priority': 399,
                                                   'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue1_Gb': {'SWBin': 54, 'HWBin': 6, 'Priority': 400,
                                                   'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue1_B': {'SWBin': 54, 'HWBin': 6, 'Priority': 401,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue2_R': {'SWBin': 54, 'HWBin': 6, 'Priority': 402,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue2_Gr': {'SWBin': 54, 'HWBin': 6, 'Priority': 403,
                                                   'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue2_Gb': {'SWBin': 54, 'HWBin': 6, 'Priority': 404,
                                                   'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue2_B': {'SWBin': 54, 'HWBin': 6, 'Priority': 405,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue3_R': {'SWBin': 54, 'HWBin': 6, 'Priority': 406,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue3_Gr': {'SWBin': 54, 'HWBin': 6, 'Priority': 407,
                                                   'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue3_Gb': {'SWBin': 54, 'HWBin': 6, 'Priority': 408,
                                                   'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue3_B': {'SWBin': 54, 'HWBin': 6, 'Priority': 409,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue4_R': {'SWBin': 54, 'HWBin': 6, 'Priority': 410,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue4_Gr': {'SWBin': 54, 'HWBin': 6, 'Priority': 411,
                                                   'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue4_Gb': {'SWBin': 54, 'HWBin': 6, 'Priority': 412,
                                                   'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_MixDCol_DASH_MaxValue4_B': {'SWBin': 54, 'HWBin': 6, 'Priority': 413,
                                                  'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_Mean_R': {'SWBin': 53, 'HWBin': 6, 'Priority': 415, 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_Mean_Gr': {'SWBin': 53, 'HWBin': 6, 'Priority': 416, 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_Mean_Gb': {'SWBin': 53, 'HWBin': 6, 'Priority': 417, 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_Mean_B': {'SWBin': 53, 'HWBin': 6, 'Priority': 418, 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_StdDEV_R': {'SWBin': 53, 'HWBin': 6, 'Priority': 419, 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_StdDEV_Gr': {'SWBin': 53, 'HWBin': 6, 'Priority': 420, 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_StdDEV_Gb': {'SWBin': 53, 'HWBin': 6, 'Priority': 421, 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'BK32X_BK_StdDEV_B': {'SWBin': 53, 'HWBin': 6, 'Priority': 422, 'IsNan': 'MIPI4L27M30F_BK32X_Cap'},
            'Binning': {'SWBin': 2, 'HWBin': 3, 'Priority': 423},
            'All Pass': {'SWBin': 255, 'HWBin': 3, 'Priority': 424}
        }
}


def ParseFile(file, _signal, analysisFolder):
    """
    parse file
    get basic information,datacheck result,binningcheck result,nanchipno result and summary result
    """
    global currentRowCount
    parseResult = {}
    global highLimitRowNum
    data = []
    # get file data
    with open(file) as f:
        csvReader = reader(f)
        for row in csvReader:
            data.append(row)

    # get row and column of last test item
    if project == 'F28':
        searchLastTestItem = SearchString(data, 'Full_Error')
    elif project == 'JX828':
        searchLastTestItem = SearchString(data, 'ChipVer')
    elif project == 'JX825':
        searchLastTestItem = SearchString(data, 'SRAM_0x56_Read')
    if not searchLastTestItem:
        exit()
    else:
        testItemRowNum = searchLastTestItem[0]
        lastTestItemColNum = searchLastTestItem[1]
    highLimitRowNum = testItemRowNum + 2
    lowLimitRowNum = testItemRowNum + 3

    # get row and column of last DC test item
    searchPwdnTotal = SearchString(data, 'PWDN_Total')
    if not searchPwdnTotal:
        exit()
    else:
        pwdnTotalColNum = searchPwdnTotal[1]

    # get row and column of Binning
    searchBinning = SearchString(data, 'Binning')
    if not searchBinning:
        exit()
    else:
        binningColNum = searchBinning[1]

    # get column of iic_test
    searchIICTest = SearchString(data, 'iic_test')
    if not searchIICTest:
        exit()
    else:
        IICTestColNum = searchIICTest[1]

    # get row of first register
    firstRegisterRowNum = len(data)
    for i in range(testItemRowNum + rowOffset, len(data)):
        try:
            int(data[i][0])
        except:
            firstRegisterRowNum = i
            break

    # fill '' to align with last test item col num
    for i in range(0, len(data)):
        addCount = lastTestItemColNum + 1 - len(data[i])
        if addCount > 0:
            for j in range(addCount):
                data[i].append('')

    # parse file name
    fileName = basename(file).split('.')[0]
    # calculate chip count
    chipCount = firstRegisterRowNum - testItemRowNum - rowOffset
    # get lotNo
    lotNo = data[5][1]

    if analysisItem in ('All', 'Data Check'):
        rowCount = len(data)

        # get row number with null value
        existNanRowList = []
        for i in range(testItemRowNum + rowOffset, firstRegisterRowNum):
            for j in range(binningColNum + 1):
                if len(data[i][j].strip()) == 0:
                    existNanRowList.append(i)
                    break

        dataCheckResult = []
        for rowNum in range(rowCount):
            rowData = []
            for colNum in range(lastTestItemColNum + 1):
                testItemName = data[testItemRowNum][colNum].strip()
                value = data[rowNum][colNum]
                if colOffset <= colNum <= binningColNum and highLimitRowNum <= rowNum <= lowLimitRowNum:
                    # fill color of limit value is green
                    rowData.append((value, '008000'))
                elif colNum == 0 and rowNum in existNanRowList:
                    # fill color of first value of exist nan row is purple
                    rowData.append((value, 'A020F0'))
                elif colOffset <= colNum <= binningColNum and testItemRowNum + rowOffset <= rowNum < firstRegisterRowNum:
                    try:
                        valueConvert = float(value)
                        highLimitData = data[highLimitRowNum][colNum]
                        try:
                            highLimit = float(highLimitData)
                        except:
                            highLimit = highLimitData
                        lowLimitData = data[lowLimitRowNum][colNum]
                        try:
                            lowLimit = float(lowLimitData)
                        except:
                            lowLimit = lowLimitData
                        if valueConvert == int(valueConvert):
                            valueConvert = int(valueConvert)
                        if (testItemName == 'AVDD_O/S' and project == 'JX828') or highLimit == 'N' or (
                                        highLimit != 'N' and lowLimit <= valueConvert <= highLimit):
                            # fill color of following scenario value is white
                            # 1.JX828 ignore AVDD_O/S
                            # 2.limit is N
                            # 3.limit is not N and data wihtin limit
                            rowData.append((valueConvert, 'FFFFFF'))
                        else:
                            # fill color of over limit is red
                            rowData.append((valueConvert, 'FF0000'))
                    except:
                        if not value.strip():
                            # fill color of '' is purple
                            rowData.append((value, 'A020F0'))
                        elif colNum == IICTestColNum:
                            if value == '1':
                                # fill color of iic_test 1 is white
                                rowData.append((valueConvert, 'FFFFFF'))
                            else:
                                # fill color of iic_test not 1 is yellow
                                rowData.append((value, 'FFFF00'))
                else:
                    # set '' when value is nan
                    if isinstance(value, float) and isnan(value):
                        value = ''
                    # fill color is white
                    rowData.append((value, 'FFFFFF'))
            dataCheckResult.append(rowData)
            currentRowCount += 1
            if currentRowCount != totalRowCount:
                _signal.emit(str(currentRowCount * 100 // totalRowCount))

        dataCheckFile = join(analysisFolder, fileName + '_DataCheck_Analysis' + nowTime + '.xlsx')
        dataCheckWb = Workbook()  # create file object
        dataCheckSheet = dataCheckWb.active  # get first sheet
        dataCheckSheet.freeze_panes = 'E17'  # set freeze panes
        irow = 1
        for i in range(len(dataCheckResult)):
            for j in range(len(dataCheckResult[i])):
                dataCheckSheet.cell(row=irow, column=j + 1).value = dataCheckResult[i][j][0]
                dataCheckSheet.cell(row=irow, column=j + 1).fill = PatternFill(fill_type='solid',
                                                                               fgColor=dataCheckResult[i][j][1])
                dataCheckSheet.cell(row=irow, column=j + 1).border = border
            irow += 1
            currentRowCount += 1
            if currentRowCount != totalRowCount:
                _signal.emit(str(currentRowCount * 100 // totalRowCount))
        dataCheckWb.save(dataCheckFile)
    if analysisItem in ('All', 'Binning Check'):
        binDefinition = binDefinitionList[project]
        binningCheckResult = []
        for rowNum in range(testItemRowNum + rowOffset, firstRegisterRowNum):
            # set currentTestItem is All Pass
            currentTestItem = 'All Pass'
            for colNum in range(colOffset, binningColNum + 1):
                testItem = data[testItemRowNum][colNum].strip()
                if testItem == 'AVDD_O/S' and project == 'JX828':
                    # JX828 skip AVDD_O/S
                    continue
                else:
                    highLimitData = data[highLimitRowNum][colNum]
                    lowLimitData = data[lowLimitRowNum][colNum]
                try:
                    highLimit = float(highLimitData)
                    lowLimit = float(lowLimitData)
                    try:
                        value = data[rowNum][colNum]
                        valueConvert = float(value)
                        if valueConvert == int(valueConvert):
                            valueConvert = int(valueConvert)
                        if valueConvert < lowLimit or highLimit < valueConvert:
                            # over limit
                            if binDefinition[testItem]['Priority'] < binDefinition[currentTestItem]['Priority']:
                                # set currentTestItem is testItem when testItem's priority less than currentTestItem's priority
                                currentTestItem = testItem
                    except:
                        # value is ''
                        if testItem in binDefinition.keys() and 'IsNan' in binDefinition[testItem].keys() and \
                                        binDefinition[binDefinition[testItem]['IsNan']]['Priority'] < \
                                        binDefinition[currentTestItem]['Priority']:
                            # set currentTestItem is binDefinition[testItem]['IsNan']
                            # when testItem in keys and InNan in keys
                            # and binDefinition[testItem]['IsNan']'s priority less than currentTestItem's priority
                            currentTestItem = binDefinition[testItem]['IsNan']
                        elif testItem in binDefinition.keys() and 'IsNan' not in binDefinition[testItem].keys() and \
                                        binDefinition[testItem]['Priority'] < \
                                        binDefinition[currentTestItem]['Priority']:
                            # set currentTestItem is testItem
                            # when testItem in keys and InNan not in keys
                            # and testItem's priority less than currentTestItem's priority
                            currentTestItem = testItem
                except:
                    # limit is N or nan
                    try:
                        value = data[rowNum][colNum]
                        float(value)
                        if testItem == 'iic_test' and value == '0':
                            if binDefinition[testItem]['Priority'] < binDefinition[currentTestItem]['Priority']:
                                # set currentTestItem is binDefinition[testItem]['IsNan']
                                # when binDefinition[testItem]['IsNan']'s priority less than currentTestItem's priority
                                currentTestItem = testItem
                    except:
                        # value is ''
                        if testItem in binDefinition.keys() and 'IsNan' in binDefinition[testItem].keys() and \
                                        binDefinition[binDefinition[testItem]['IsNan']]['Priority'] < \
                                        binDefinition[currentTestItem]['Priority']:
                            # set currentTestItem is binDefinition[testItem]['IsNan']
                            # when testItem in keys and InNan in keys
                            # and binDefinition[testItem]['IsNan']'s priority less than currentTestItem's priority
                            currentTestItem = binDefinition[testItem]['IsNan']
                        elif testItem in binDefinition.keys() and 'IsNan' not in binDefinition[testItem].keys() and \
                                        binDefinition[testItem]['Priority'] < binDefinition[currentTestItem][
                                    'Priority']:
                            # set currentTestItem is testItem
                            # when testItem in keys and InNan not in keys
                            # and testItem's priority less than currentTestItem's priority
                            currentTestItem = testItem
            if binDefinition[currentTestItem]['SWBin'] != int(data[rowNum][2]):
                # currentTestItem's SWBin is not equal to SW_BIN in csv file
                binningCheckResult.append(
                    "              SB_BIN error of chipNo " + data[rowNum][
                        0] + " : according to the priority,swbin should be " + str(
                        binDefinition[currentTestItem]['SWBin']) + " ,but in CSV it's " + data[rowNum][2] + "\n")
            if binDefinition[currentTestItem]['HWBin'] != int(data[rowNum][3]):
                # currentTestItem's HWBin is not equal to hW_BIN in csv file
                binningCheckResult.append(
                    "              hW_BIN error of chipNo " + data[rowNum][
                        0] + " : according to the priority,hwbin should be " + str(
                        binDefinition[currentTestItem]['HWBin']) + " ,but in CSV it's " + data[rowNum][3] + "\n")
            currentRowCount += 1
            if currentRowCount != totalRowCount:
                _signal.emit(str(currentRowCount * 100 // totalRowCount))
        binningCheckFile = join(analysisFolder, lotNo + '_BinningCheck_Analysis' + nowTime + '.txt')
        with open(binningCheckFile, 'a') as f:
            f.write("            " + fileName + "：\n")
            if len(binningCheckResult) > 0:
                for item in binningCheckResult:
                    f.write(item)
            else:
                f.write('              No problem.\n')
    if analysisItem in ('All', 'Nan ChipNo'):
        dcNanChipno = []
        imageNanChipno = []
        for i in range(testItemRowNum + rowOffset, firstRegisterRowNum):
            for j in range(colOffset, pwdnTotalColNum + 1):
                if len(data[i][j].strip()) == 0:
                    # append value which is '' in columns colOffset to pwdnTotalColNum
                    dcNanChipno.append(data[i][0])
                    break
        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))
        for i in range(testItemRowNum + rowOffset, firstRegisterRowNum):
            for j in range(pwdnTotalColNum + 1, binningColNum + 1):
                if len(data[i][j].strip()) == 0:
                    # append value which is '' in columns pwdnTotalColNum+1 to binningColNum
                    imageNanChipno.append(data[i][0])
                    break
        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))
        nanChipnoFile = join(analysisFolder, lotNo + '_NanChipno_Analysis' + nowTime + '.txt')
        dcCount = len(dcNanChipno)
        imageCount = len(imageNanChipno)
        with open(nanChipnoFile, 'a') as f:
            f.write("            " + fileName + "：\n")
            if dcCount > 0 or imageCount > 0:
                if dcCount == 0:
                    f.write("              (1) DC : no nan value.\n")
                else:
                    f.write("              (1) DC : " + str(dcCount) + " in total.They are : " + str(
                        dcNanChipno) + "\n")
                if imageCount == 0:
                    f.write("              (2) IMAGE : no nan value\n")
                else:
                    f.write("              (2) IMAGE : " + str(imageCount) + " in total.They are : " + str(
                        imageNanChipno) + '\n')
            else:
                f.write("              No nan value.\n")
        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))
    if analysisItem in ('All', 'Summary'):
        summaryResult = {}
        for groupById in range(1, 4):
            # 1:Site    2:SW_BIN    3:hW_BIN
            groupName = data[testItemRowNum][groupById]
            groupList = []
            for i in range(testItemRowNum + rowOffset, firstRegisterRowNum):
                # get value
                groupList.append(int(data[i][groupById]))
            # remove duplicate value
            formatGroupList = list(set(groupList))
            # sort list
            formatGroupList.sort()

            groupIndex = {}
            for i in formatGroupList:
                temp = []
                # find i in groupList
                dataList = FindItem(groupList, i)
                if groupById == 1:
                    tempList = []
                    for j in dataList:
                        # get the corresponding SW_BIN of Site
                        tempList.append(data[testItemRowNum + rowOffset + j][2])
                    # remove duplicate value
                    formatTempList = list(set(tempList))
                    tempIndex = {}
                    for m in formatTempList:
                        # find m in tempList
                        tempDataList = FindItem(tempList, m)
                        tempIndex[m] = tempDataList
                    temp.append(tempIndex)
                else:
                    temp.append(dataList)
                testItemFailCount = []
                for colNum in range(colOffset, lastTestItemColNum + 1):
                    testItem = data[testItemRowNum][colNum].strip()
                    if testItem == 'AVDD_O/S' and project == 'JX828':
                        # set AVDD_O/S's limit in JX828 project
                        highLimitData = -0.2
                        lowLimitData = -0.6
                    else:
                        highLimitData = data[highLimitRowNum][colNum]
                        lowLimitData = data[lowLimitRowNum][colNum]
                    tempList = [data[testItemRowNum][colNum], 0]
                    try:
                        highLimit = float(highLimitData)
                        lowLimit = float(lowLimitData)
                        for j in dataList:
                            try:
                                value = data[testItemRowNum + rowOffset + j][colNum]
                                valueConvert = float(value)
                                if valueConvert == int(valueConvert):
                                    valueConvert = int(valueConvert)
                                if valueConvert < lowLimit or highLimit < valueConvert:
                                    # count+1 when value over limit
                                    tempList[1] += 1
                            except:
                                # count+1 when value is ''
                                tempList[1] += 1
                    except:
                        # limit is N or nan
                        continue
                    testItemFailCount.append(tempList)
                temp.append(testItemFailCount)
                groupIndex[i] = temp
            summaryResult[groupName] = groupIndex
            parseResult['summary'] = summaryResult
            currentRowCount += 1
            if currentRowCount != totalRowCount:
                _signal.emit(str(currentRowCount * 100 // totalRowCount))
    parseResult['chip count'] = chipCount
    parseResult['lotNo'] = lotNo
    return parseResult


def save_data(analysisFolder, _signal, parseData):
    """
    save data
    save data check,binning check,nan chipno and summary to files
    """
    global currentRowCount
    siteData = []
    softbinData = []
    hardbinData = []
    lotCount = parseData[0]['chip count']
    lotNo = parseData[0]['lotNo']
    for data in parseData:
        if analysisItem in ('All', 'Summary'):
            siteData.append(data['summary']['Site'])
            # sort softbin
            softbinData.append(
                sorted(data['summary']['SW_BIN'].items(), key=lambda item: len(item[1][0]), reverse=True))
            hardbinData.append(data['summary']['hW_BIN'])
    if analysisItem in ('All', 'Summary'):
        summaryFile = join(analysisFolder, lotNo + '_Summary_Analysis_' + nowTime + '.xlsx')
        summaryWb = Workbook()

        okHwbinCount = 0
        beginFailSwbin = 0
        for hwbinKey in hwbinToSwbin[project].keys():
            if hwbinToSwbin[project][hwbinKey]['isPassBin']:
                okHwbinCount += 1
                beginFailSwbin += len(hwbinToSwbin[project][hwbinKey]['SWBin'])

        colorList = ['99FFFF', '33FF00', 'FFFFCC', 'FFFF33', 'FF9900', 'FF0099', 'FF0000']
        swbinList = []
        keyIndex = 0
        for hwbinKey in hwbinToSwbin[project].keys():
            for swbin in hwbinToSwbin[project][hwbinKey]['SWBin']:
                swbinList.append([swbin, colorList[keyIndex]])
            keyIndex += 1

        hardbinSheet = summaryWb.create_sheet('HWBin')
        hardbinSheet.freeze_panes = 'B2'
        summaryData = []
        for i in range(len(hardbinData)):
            tempList = []
            if i == 0:
                tempList.append('FT')
            else:
                tempList.append('RT' + str(i))
            testCount = 0
            passCount = 0
            for hwbinKey in hwbinToSwbin[project].keys():
                if hwbinKey in hardbinData[i].keys():
                    binCount = len(hardbinData[i][hwbinKey][0])
                else:
                    binCount = 0
                if hwbinToSwbin[project][hwbinKey]['isPassBin']:
                    passCount += binCount
                testCount += binCount
                tempList.append(binCount)
            tempList.append(testCount)
            passPercent = '{:.2%}'.format(passCount / testCount)
            tempList.append(passPercent)
            summaryData.append(tempList)
        irow = 1
        icol = 1
        hardbinSheet.cell(row=irow, column=icol).value = lotNo
        icol += 1
        for hwbinKey in hwbinToSwbin[project].keys():
            hardbinSheet.cell(row=irow, column=icol).value = 'HWBin' + str(hwbinKey)
            icol += 1
        hardbinSheet.cell(row=irow, column=icol).value = 'TestCount'
        icol += 1
        hardbinSheet.cell(row=irow, column=icol).value = 'PassPercent'
        irow += 1
        for i in range(len(summaryData)):
            for j in range(len(summaryData[i])):
                hardbinSheet.cell(row=irow, column=(j + 1)).value = summaryData[i][j]
                if j == 0:
                    hardbinSheet.cell(row=irow, column=(j + 1)).fill = PatternFill(fill_type='solid', fgColor=GREEN)
                elif 1 <= j < len(summaryData[i]) - 2:
                    hardbinSheet.cell(row=irow + 1, column=(j + 1)).value = '{:.2%}'.format(
                        summaryData[i][j] / summaryData[i][-2])
                    hardbinSheet.cell(row=irow + 1, column=(j + 1)).fill = PatternFill(fill_type='solid',
                                                                                       fgColor=GREEN)
                elif j == len(summaryData[i]) - 2 and i > 0:
                    compareCount = 0
                    for m in range(okHwbinCount + 1, len(summaryData[i]) - 2):
                        compareCount += summaryData[i - 1][m]
                    if summaryData[i][j] != compareCount:
                        # the number of test is not equal to the total number of chips failed in the previous test
                        if summaryData[i][j] > compareCount:
                            flag = '↓'
                        else:
                            flag = '↑'
                        hardbinSheet.cell(row=irow, column=(j + 1)).fill = PatternFill(fill_type='solid', fgColor=RED)
                        hardbinSheet.cell(row=irow + 1, column=(j + 1)).value = flag + str(compareCount)
                        hardbinSheet.cell(row=irow + 1, column=(j + 1)).font = Font(color=RED, bold=True)
            irow += 2
        hardbinSheet.cell(row=irow, column=1).value = 'Summary'
        hardbinSheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=GREEN)
        # summary pass hwbin count : add all lots pass hwbin count
        passHwbinCount = [0] * okHwbinCount
        for i in range(len(summaryData)):
            for j in range(len(passHwbinCount)):
                passHwbinCount[j] += summaryData[i][j + 1]
        # summary total pass hwbin count : add all pass hwbin count
        totalPassHwbinCount = 0
        for i in range(len(passHwbinCount)):
            hardbinSheet.cell(row=irow, column=2 + i).value = passHwbinCount[i]
            totalPassHwbinCount += passHwbinCount[i]
        # summary fail hwbin count : last lot's fail hwbin count
        for i in range(len(passHwbinCount) + 1, len(summaryData[-1]) - 2):
            hardbinSheet.cell(row=irow, column=(i + 1)).value = summaryData[-1][i]
        hardbinSheet.cell(row=irow, column=icol - 1).value = summaryData[0][-2]
        hardbinSheet.cell(row=irow, column=icol).value = '{:.2%}'.format(totalPassHwbinCount / summaryData[0][-2])

        for row in hardbinSheet.rows:
            for cell in row:
                cell.border = border
                if cell.row == 1:
                    cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                    cell.font = Font(bold=True)
                    cell.alignment = alignment
                if cell.row == 2 and cell.column == hardbinSheet.max_column:
                    cell.fill = PatternFill(fill_type='solid', fgColor=GREEN)
                if cell.row == hardbinSheet.max_row and cell.column == hardbinSheet.max_column:
                    cell.fill = PatternFill(fill_type='solid', fgColor=GREEN)

        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))

        hardsoftbinSheet = summaryWb.create_sheet('HWBin-SWBin')
        hardsoftbinSheet.freeze_panes = 'C2'
        irow = 1
        hardsoftbinSheet.cell(row=irow, column=1).value = lotNo
        hardsoftbinSheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
        hardsoftbinSheet.cell(row=irow, column=3).value = 'FT'
        hardsoftbinSheet.cell(row=irow, column=3).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
        hardsoftbinSheet.merge_cells(start_row=irow, end_row=irow, start_column=3, end_column=4)
        for i in range(1, len(softbinData)):
            hardsoftbinSheet.cell(row=irow, column=3 + 2 * i).value = 'RT' + str(i)
            hardsoftbinSheet.cell(row=irow, column=3 + 2 * i).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
            hardsoftbinSheet.merge_cells(start_row=irow, end_row=irow, start_column=3 + 2 * i, end_column=4 + 2 * i)
        irow += 1

        # sort swbin in hwbin from FT by swbin count from more to less
        swbinSortByFTList = []
        for hwbinKey in hwbinToSwbin[project].keys():
            tempList = []
            for swbin in hwbinToSwbin[project][hwbinKey]['SWBin']:
                findSoftbin = False
                for x in range(len(softbinData[0])):
                    if swbin == softbinData[0][x][0]:
                        findSoftbin = True
                        swbinCount = len(softbinData[0][x][1][0])
                        tempList.append((swbin, swbinCount))
                        break
                if not findSoftbin:
                    tempList.append((swbin, 0))
            for m in range(len(tempList) - 1):
                for n in range(m + 1, len(tempList)):
                    if tempList[m][1] < tempList[n][1]:
                        tempList[m], tempList[n] = tempList[n], tempList[m]
            tempCountList = [hwbinKey]
            for y in range(len(tempList)):
                tempCountList.append(tempList[y][0])
            swbinSortByFTList.append(tempCountList)

        summarySoftCount = []
        for i in range(len(swbinSortByFTList)):
            hardsoftbinSheet.cell(row=irow, column=1).value = 'HWBin' + str(swbinSortByFTList[i][0])
            hardsoftbinSheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=GREEN)
            hardsoftbinSheet.cell(row=irow, column=1).font = Font(bold=True)
            for j in range(1, len(swbinSortByFTList[i])):
                hardsoftbinSheet.cell(row=irow, column=2).value = 'SWBin' + str(swbinSortByFTList[i][j])
                tempCount = 0
                for m in range(len(softbinData)):
                    findSoftbin = False
                    for n in range(len(softbinData[m])):
                        if swbinSortByFTList[i][j] == softbinData[m][n][0]:
                            findSoftbin = True
                            swbinCount = len(softbinData[m][n][1][0])
                            break
                    if not findSoftbin:
                        swbinCount = 0
                    if i in range(okHwbinCount):
                        # add the number of pass hwbin's swbin of all lots
                        tempCount += swbinCount
                    elif m == len(softbinData) - 1:
                        # set the number of fail hwbin's swbin of last lot
                        tempCount = swbinCount
                    hardsoftbinSheet.cell(row=irow, column=(2 * m + 3)).value = swbinCount
                    hardsoftbinSheet.cell(row=irow, column=(2 * m + 4)).value = '{:.2%}'.format(
                        swbinCount / summaryData[0][-2])
                    hardsoftbinSheet.cell(row=irow, column=(2 * m + 4)).fill = PatternFill(fill_type='solid',
                                                                                           fgColor=GREEN)
                irow += 1
                summarySoftCount.append(tempCount)
            summarySoftCount.append('')
            irow += 1

        irow = 1
        icol = 4 + 2 * len(softbinData)
        hardsoftbinSheet.cell(row=irow, column=icol).value = 'Summary'
        hardsoftbinSheet.cell(row=irow, column=icol).fill = PatternFill(fill_type='solid', fgColor='FFA500')
        hardsoftbinSheet.merge_cells(start_row=irow, end_row=irow, start_column=icol, end_column=icol + 1)
        irow += 1
        for i in range(len(summarySoftCount)):
            if isinstance(summarySoftCount[i], int):
                hardsoftbinSheet.cell(row=irow, column=icol).value = summarySoftCount[i]
                hardsoftbinSheet.cell(row=irow, column=icol + 1).value = '{:.2%}'.format(
                    summarySoftCount[i] / summaryData[0][-2])
                hardsoftbinSheet.cell(row=irow, column=icol + 1).fill = PatternFill(fill_type='solid',
                                                                                    fgColor='FFA500')
            irow += 1

        for row in hardsoftbinSheet.rows:
            for cell in row:
                cell.border = border
                if cell.row == 1:
                    cell.font = Font(bold=True)
                    cell.alignment = alignment

        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))

        sitesoftbinSheet = summaryWb.create_sheet('Site-SWBin')
        sitesoftbinSheet.freeze_panes = 'B2'
        irow = 1
        sitesoftbinSheet.cell(row=irow, column=1).value = lotNo
        sitesoftbinSheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
        for i in range(16):
            sitesoftbinSheet.cell(row=irow, column=2 + i).value = 'Site' + str(i)
            sitesoftbinSheet.cell(row=irow, column=2 + i).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
        sitesoftbinSheet.merge_cells(start_row=irow, end_row=irow, start_column=19, end_column=20)
        sitesoftbinSheet.cell(row=irow, column=19).value = 'Summary'
        sitesoftbinSheet.cell(row=irow, column=19).fill = PatternFill(fill_type='solid', fgColor='FFA500')
        irow += 1

        lotNoSiteSwbinCount = []
        for x in range(len(swbinList)):
            siteCountList = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                             [11, 0], [12, 0], [13, 0], [14, 0], [15, 0]]
            swbin = str(swbinList[x][0])
            for site in range(16):
                if x < beginFailSwbin:
                    for i in range(len(siteData)):
                        if (site in siteData[i].keys()) and (swbin in siteData[i][site][0].keys()):
                            siteCountList[site][1] += len(siteData[i][site][0][swbin])
                else:
                    if (site in siteData[-1].keys()) and (swbin in siteData[-1][site][0].keys()):
                        siteCountList[site][1] += len(siteData[-1][site][0][swbin])
            lotNoSiteSwbinCount.append(siteCountList)
        siteSwbinCount = []
        for i in range(len(lotNoSiteSwbinCount)):
            tempTotalCount = 0
            tempList = [0] * 16
            tempSwbinCount = []
            for j in range(len(tempList)):
                tempList[j] += lotNoSiteSwbinCount[i][j][1]
                tempSwbinCount.append([tempList[j], WHITE])
                tempTotalCount += tempList[j]
                if j == len(tempList) - 1:
                    tempSwbinCount.append([tempTotalCount, 'FFA500'])
            siteSwbinCount.append(tempSwbinCount)
        # add the number of fail swbin by all site
        # fill color of max value in fail swbin is green(all values are 0 do not fill green)
        # fill color of min value in fail swbin is red(multiple values of 0 do not fill red)
        sitePassTotalList = [0] * 16
        for i in range(beginFailSwbin):
            for j in range(len(siteSwbinCount[i]) - 1):
                sitePassTotalList[j] += siteSwbinCount[i][j][0]
        siteFailTotalList = [0] * 16
        for i in range(beginFailSwbin, len(siteSwbinCount)):
            minValue = siteSwbinCount[i][0][0]
            maxValue = siteSwbinCount[i][0][0]
            for m in range(1, len(siteSwbinCount[i]) - 1):
                if minValue > siteSwbinCount[i][m][0]:
                    minValue = siteSwbinCount[i][m][0]
                if maxValue < siteSwbinCount[i][m][0]:
                    maxValue = siteSwbinCount[i][m][0]
            minIndex = []
            maxIndex = []
            for j in range(len(siteSwbinCount[i]) - 1):
                siteFailTotalList[j] += siteSwbinCount[i][j][0]
                if siteSwbinCount[i][j][0] == minValue:
                    minIndex.append(j)
                if siteSwbinCount[i][j][0] == maxValue:
                    maxIndex.append(j)
            if minValue == 0 and len(minIndex) == 1:
                siteSwbinCount[i][minIndex[0]][1] = GREEN
                for y in range(len(maxIndex)):
                    siteSwbinCount[i][maxIndex[y]][1] = RED
            elif minValue == 0 and maxValue > 0:
                for y in range(len(maxIndex)):
                    siteSwbinCount[i][maxIndex[y]][1] = RED
            elif minValue > 0:
                for x in range(len(minIndex)):
                    siteSwbinCount[i][minIndex[x]][1] = GREEN
                for y in range(len(maxIndex)):
                    siteSwbinCount[i][maxIndex[y]][1] = RED

        for x in range(len(swbinList)):
            sitesoftbinSheet.cell(row=irow, column=1).value = 'SWBin' + str(swbinList[x][0])
            sitesoftbinSheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=swbinList[x][1])
            for y in range(len(siteSwbinCount[x])):
                if y < len(siteSwbinCount[x]) - 1:
                    if siteSwbinCount[x][y][0] > 0:
                        sitesoftbinSheet.cell(row=irow, column=2 + y).value = '{:.4%}'.format(
                            siteSwbinCount[x][y][0] / summaryData[0][-2])
                    sitesoftbinSheet.cell(row=irow, column=2 + y).fill = PatternFill(fill_type='solid',
                                                                                     fgColor=siteSwbinCount[x][y][1])
                else:
                    sitesoftbinSheet.cell(row=irow, column=3 + y).value = siteSwbinCount[x][y][0]
                    sitesoftbinSheet.cell(row=irow, column=4 + y).value = '{:.4%}'.format(
                        siteSwbinCount[x][y][0] / summaryData[0][-2])
                    sitesoftbinSheet.cell(row=irow, column=4 + y).fill = PatternFill(fill_type='solid',
                                                                                     fgColor=siteSwbinCount[x][y][1])
            irow += 1
        irow += 1
        sitesoftbinSheet.merge_cells(start_row=irow, end_row=irow + 1, start_column=1, end_column=1)
        sitesoftbinSheet.cell(row=irow, column=1).value = 'FailPercent'
        sitesoftbinSheet.cell(row=irow, column=1).font = Font(bold=True)
        sitesoftbinSheet.cell(row=irow, column=1).alignment = alignment
        sitesoftbinSheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor='FFA500')
        for i in range(len(siteFailTotalList)):
            sitesoftbinSheet.cell(row=irow, column=2 + i).value = siteFailTotalList[i]
            sitesoftbinSheet.cell(row=irow + 1, column=2 + i).value = '{:.4%}'.format(
                siteFailTotalList[i] / summaryData[0][-2])
            sitesoftbinSheet.cell(row=irow + 1, column=2 + i).fill = PatternFill(fill_type='solid', fgColor=RED)
        sitesoftbinSheet.cell(row=irow, column=3 + len(siteFailTotalList)).value = sum(siteFailTotalList)
        sitesoftbinSheet.cell(row=irow, column=3 + len(siteFailTotalList)).fill = PatternFill(fill_type='solid',
                                                                                              fgColor=RED)
        sitesoftbinSheet.cell(row=irow + 1, column=3 + len(siteFailTotalList)).value = '{:.4%}'.format(
            sum(siteFailTotalList) / summaryData[0][-2])
        sitesoftbinSheet.cell(row=irow + 1, column=3 + len(siteFailTotalList)).fill = PatternFill(fill_type='solid',
                                                                                                  fgColor=RED)
        irow += 2
        sitesoftbinSheet.merge_cells(start_row=irow, end_row=irow + 1, start_column=1, end_column=1)
        sitesoftbinSheet.cell(row=irow, column=1).value = 'PassPercent'
        sitesoftbinSheet.cell(row=irow, column=1).font = Font(bold=True)
        sitesoftbinSheet.cell(row=irow, column=1).alignment = alignment
        sitesoftbinSheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=GREEN)
        for i in range(len(sitePassTotalList)):
            sitesoftbinSheet.cell(row=irow, column=2 + i).value = sitePassTotalList[i]
            sitesoftbinSheet.cell(row=irow + 1, column=2 + i).value = '{:.4%}'.format(
                sitePassTotalList[i] / summaryData[0][-2])
            sitesoftbinSheet.cell(row=irow + 1, column=2 + i).fill = PatternFill(fill_type='solid', fgColor=GREEN)
        sitesoftbinSheet.cell(row=irow, column=3 + len(sitePassTotalList)).value = sum(sitePassTotalList)
        sitesoftbinSheet.cell(row=irow, column=3 + len(sitePassTotalList)).fill = PatternFill(fill_type='solid',
                                                                                              fgColor=GREEN)
        sitesoftbinSheet.cell(row=irow + 1, column=3 + len(sitePassTotalList)).value = '{:.4%}'.format(
            sum(sitePassTotalList) / summaryData[0][-2])
        sitesoftbinSheet.cell(row=irow + 1, column=3 + len(sitePassTotalList)).fill = PatternFill(fill_type='solid',
                                                                                                  fgColor=GREEN)
        for row in sitesoftbinSheet.rows:
            for cell in row:
                cell.border = border
                if cell.row == 1:
                    cell.font = Font(bold=True)
                    cell.alignment = alignment

        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))

        hwbinTestItemSheet = summaryWb.create_sheet('HWBin-TestItem')
        hwbinTestItemSheet.freeze_panes = 'B2'
        irow = 1
        hwbinTestItemSheet.cell(row=irow, column=1).value = lotCount
        for hwbinKey in hardbinData[0].keys():
            for i in range(len(hardbinData[0][hwbinKey][1])):
                hwbinTestItemSheet.cell(row=irow, column=i + 2).value = hardbinData[0][hwbinKey][1][i][0]
            break
        irow += 1
        for hwbinKey in hardbinData[0].keys():
            hwbinTestItemSheet.cell(row=irow, column=1).value = 'HWBin' + str(hwbinKey)
            hwbinTestItemSheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=GREEN)
            for i in range(len(hardbinData[0][hwbinKey][1])):
                hwbinTestItemSheet.cell(row=irow, column=2 + i).value = hardbinData[0][hwbinKey][1][i][1]
                hwbinTestItemSheet.cell(row=irow + 1, column=2 + i).value = '{:.2%}'.format(
                    hardbinData[0][hwbinKey][1][i][1] / lotCount)
                if hardbinData[0][hwbinKey][1][i][1] > 0:
                    # percent value greater than 0 are filled in red
                    hwbinTestItemSheet.cell(row=irow + 1, column=2 + i).fill = PatternFill(fill_type='solid',
                                                                                           fgColor=RED)
            irow += 2

        for row in hwbinTestItemSheet.rows:
            for cell in row:
                cell.border = border
                if cell.row == 1 and cell.column > 1:
                    cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                    cell.font = Font(bold=True)
                    cell.alignment = alignment

        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))

        swbinTestItemSheet = summaryWb.create_sheet('SWBin-TestItem')
        swbinTestItemSheet.freeze_panes = 'B2'
        irow = 1
        swbinTestItemSheet.cell(row=irow, column=1).value = lotCount
        for i in range(len(softbinData[0][0][1][1])):
            swbinTestItemSheet.cell(row=irow, column=i + 2).value = softbinData[0][0][1][1][i][0]
        irow += 1
        for x in range(len(swbinList)):
            swbinTestItemSheet.cell(row=irow, column=1).value = 'SWBin' + str(swbinList[x][0])
            swbinTestItemSheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid',
                                                                           fgColor=swbinList[x][1])
            for i in range(len(softbinData[0])):
                if swbinList[x][0] == softbinData[0][i][0]:
                    for j in range(len(softbinData[0][i][1][1])):
                        swbinTestItemSheet.cell(row=irow, column=2 + j).value = softbinData[0][i][1][1][j][1]
                        swbinTestItemSheet.cell(row=irow + 1, column=2 + j).value = '{:.2%}'.format(
                            softbinData[0][i][1][1][j][1] / lotCount)
                        if softbinData[0][i][1][1][j][1] > 0:
                            # percent value greater than 0 are filled in red
                            swbinTestItemSheet.cell(row=irow + 1, column=2 + j).fill = PatternFill(fill_type='solid',
                                                                                                   fgColor=RED)
            irow += 2

        for row in swbinTestItemSheet.rows:
            for cell in row:
                cell.border = border
                if cell.row == 1 and cell.column > 1:
                    cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                    cell.font = Font(bold=True)
                    cell.alignment = alignment

        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))

        siteTestItemSheet = summaryWb.create_sheet('Site-TestItem')
        siteTestItemSheet.freeze_panes = 'B2'
        irow = 1
        siteTestItemSheet.cell(row=irow, column=1).value = lotCount
        for siteKey in siteData[0].keys():
            for i in range(len(siteData[0][siteKey][1])):
                siteTestItemSheet.cell(row=irow, column=i + 2).value = siteData[0][siteKey][1][i][0]
            break
        irow += 1
        for siteKey in siteData[0].keys():
            siteTestItemSheet.cell(row=irow, column=1).value = 'Site' + str(siteKey)
            siteTestItemSheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid',
                                                                          fgColor=GREEN)
            for i in range(len(siteData[0][siteKey][1])):
                siteTestItemSheet.cell(row=irow, column=2 + i).value = siteData[0][siteKey][1][i][1]
                siteTestItemSheet.cell(row=irow + 1, column=2 + i).value = '{:.2%}'.format(
                    siteData[0][siteKey][1][i][1] / lotCount)
                if siteData[0][siteKey][1][i][1] > 0:
                    # percent value greater than 0 are filled in red
                    siteTestItemSheet.cell(row=irow + 1, column=2 + i).fill = PatternFill(fill_type='solid',
                                                                                          fgColor=RED)
            irow += 2

        for row in siteTestItemSheet.rows:
            for cell in row:
                cell.border = border
                if cell.row == 1 and cell.column > 1:
                    cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                    cell.font = Font(bold=True)
                    cell.alignment = alignment

        for sheet_name in summaryWb.sheetnames:
            if sheet_name == 'Sheet':
                del summaryWb[sheet_name]
            else:
                SetColumnWidth(summaryWb[sheet_name])
        summaryWb.save(summaryFile)
        currentRowCount += 1
        if currentRowCount != totalRowCount:
            _signal.emit(str(currentRowCount * 100 // totalRowCount))


class Runthread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self, openPath, chooseRadio):
        super(Runthread, self).__init__()
        self.openPath = openPath
        self.chooseRadio = chooseRadio

    def __del__(self):
        self.wait()

    def run(self):
        if self.chooseRadio == 'DateFolder':
            lotNoNames = listdir(self.openPath)
            for name in lotNoNames:
                folder = join(self.openPath, name)
                if isdir(folder):
                    # get CSV file under the folder
                    fileList = GetFileList(folder, '.csv')
                    if not fileList:
                        exit()

                    # analysis folder path
                    if argv.count('-a') == 0:
                        # default analysis folder
                        analysisFolder = folder + '\Analysis'
                    else:
                        analysisFolder = argv[argv.index('-a') + 1]

                    # create analysis folder
                    MkDir(analysisFolder)

                    parseData = []
                    for file in fileList:
                        # parse file
                        parseData.append(ParseFile(file, self._signal, analysisFolder))
                    # save data
                    save_data(analysisFolder, self._signal, parseData)
        else:
            fileList = GetFileList(self.openPath, '.csv')
            if not fileList:
                exit()

            # analysis folder path
            if argv.count('-a') == 0:
                # default analysis folder
                analysisFolder = self.openPath + '\Analysis'
            else:
                analysisFolder = argv[argv.index('-a') + 1]

            # create analysis folder
            MkDir(analysisFolder)

            parseData = []
            for file in fileList:
                # parse file
                parseData.append(ParseFile(file, self._signal, analysisFolder))
            # save data
            save_data(analysisFolder, self._signal, parseData)
        self._signal.emit(str(100))


class MainWindow(QMainWindow, Datalog_DateLot_Analysis_UI.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.cwd = getcwd()
        self.qe = QErrorMessage(self)
        self.pale = QPalette()
        self.pale.setBrush(self.backgroundRole(), QBrush(QPixmap('./images/kobe3.jpg')))
        self.setPalette(self.pale)
        # click button call openfolder
        self.Open_pushButton.clicked.connect(self.Open)
        self.Project_comboBox.insertItem(0, self.tr('F28'))
        self.Project_comboBox.insertItem(1, self.tr('JX828'))
        self.Project_comboBox.insertItem(2, self.tr('JX825'))
        self.AnalysisItem_comboBox.insertItem(0, self.tr('All'))
        self.AnalysisItem_comboBox.insertItem(1, self.tr('Summary'))
        self.AnalysisItem_comboBox.insertItem(2, self.tr('Data Check'))
        self.AnalysisItem_comboBox.insertItem(3, self.tr('Binning Check'))
        self.AnalysisItem_comboBox.insertItem(4, self.tr('Nan ChipNo'))
        self.Analysis_pushButton.clicked.connect(self.Analysis)

    def Open(self):
        if self.DateFolder_radioButton.isChecked():
            dirChoose = QFileDialog.getExistingDirectory(self, 'Select DateFolder Directory', self.cwd)
        else:
            dirChoose = QFileDialog.getExistingDirectory(self, 'Select LotFolder Directory', self.cwd)
        if not dirChoose:
            return
        self.Open_lineEdit.setText(dirChoose)

    def CallBackLog(self, msg):
        self.progressBar.setValue(int(msg))  # pass the thread's parameters to progressBar
        if msg == '100':
            self.Analysis_pushButton.setEnabled(True)

    def Analysis(self):
        if not self.Open_lineEdit.text():
            self.qe.showMessage('Path cannot be empty!')
            return
        else:
            global totalRowCount
            totalRowCount = 0
            global analysisItem
            analysisItem = self.AnalysisItem_comboBox.currentText()
            if self.DateFolder_radioButton.isChecked():
                lotNoNames = listdir(self.Open_lineEdit.text())
                for lotName in lotNoNames:
                    lotFolder = join(self.Open_lineEdit.text(), lotName)
                    if isdir(lotFolder):
                        fileList = GetFileList(lotFolder, '.csv')
                        for file in fileList:
                            with open(file, encoding='unicode_escape') as f:
                                csvReader = reader(f)
                                if analysisItem == 'All':
                                    totalRowCount += (array(list(csvReader)).shape[0] * 3)
                                    totalRowCount += 12
                                elif analysisItem == 'Data Check':
                                    totalRowCount += (array(list(csvReader)).shape[0] * 2)
                                elif analysisItem == 'Binning Check':
                                    totalRowCount += (array(list(csvReader)).shape[0])
                                elif analysisItem == 'Nan ChipNo':
                                    totalRowCount += 3
                                elif analysisItem == 'Summary':
                                    totalRowCount += 9
            else:
                fileList = GetFileList(self.Open_lineEdit.text(), '.csv')
                for file in fileList:
                    with open(file, encoding='unicode_escape') as f:
                        csvReader = reader(f)
                        if analysisItem == 'All':
                            totalRowCount += (array(list(csvReader)).shape[0] * 3)
                            totalRowCount += 12
                        elif analysisItem == 'Data Check':
                            totalRowCount += (array(list(csvReader)).shape[0] * 2)
                        elif analysisItem == 'Binning Check':
                            totalRowCount += (array(list(csvReader)).shape[0])
                        elif analysisItem == 'Nan ChipNo':
                            totalRowCount += 3
                        elif analysisItem == 'Summary':
                            totalRowCount += 9
            if totalRowCount == 0:
                self.qe.showMessage('No files available!')
                return
            global nowTime
            nowTime = datetime.now().strftime("%Y%m%d%H%M%S")
            global currentRowCount
            currentRowCount = 0
            self.progressBar.setValue(0)
            global project
            project = self.Project_comboBox.currentText()
            if self.DateFolder_radioButton.isChecked():
                chooseRadio = self.DateFolder_radioButton.text()
            else:
                chooseRadio = self.LotFolder_radioButton.text()
            # create thread
            self.Analysis_pushButton.setEnabled(False)
            self.thread = Runthread(self.Open_lineEdit.text(), chooseRadio)
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
