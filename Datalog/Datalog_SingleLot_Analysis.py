# encoding:utf-8
# @Time     : 2019/9/9 13:32
# @Author   : Jerry Chou
# @File     :
# @Function :

from csv import reader
from os.path import basename, isdir, join, exists
from os import listdir, makedirs
from datetime import datetime
from math import isnan
from sys import argv
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.styles.colors import YELLOW, GREEN, BLACK, WHITE, RED
from progressbar import *
from openpyxl.utils import get_column_letter


def find_item(item_list, value):
    """
    find value in item list
    """
    return [i for i, v in enumerate(item_list) if v == value]


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


def set_column_width(sheet):
    """
    set column width
    """
    # get the maximum width of each column
    col_width = [0.5] * sheet.max_column
    for row in range(sheet.max_row):
        for col in range(sheet.max_column):
            value = sheet.cell(row=row + 1, column=col + 1).value
            if value:
                width = len(str(value))
                if width > col_width[col]:
                    col_width[col] = width
    # set column width
    for i in range(len(col_width)):
        col_lettert = get_column_letter(i + 1)
        if col_width[i] > 100:
            # set to 100 if col_width greater than 100
            sheet.column_dimensions[col_lettert].width = 100
        else:
            sheet.column_dimensions[col_lettert].width = col_width[i] + 4


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


def sort_data(data):
    """
    sort from more to less according to the number of child node elements
    """
    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            if len(data[i][1]) < len(data[j][1]):
                data[i], data[j] = data[j], data[i]


row_offset = 5
col_offset = 4
high_limit_row_num = 0
# default project
project_id = 0
# get current time
now_time = datetime.now().strftime("%Y%m%d%H%M")
# water green
golden_data_color = '00FFFF'
alignment = Alignment(horizontal='center', vertical='center')
thin = Side(border_style='thin', color=BLACK)
border = Border(top=thin, left=thin, right=thin, bottom=thin)

hwbin_to_swbin_list = [
    [
        [1, [1, 2]],
        [2, [41, 42, 43, 44, 45, 53, 54, 55]],
        [4, [23, 24, 25, 29, 30, 33, 34, 36, 39, 40, 70, 71, 72]],
        [5, [5, 6, 7, 8, 9, 12, 96, 97, 98, 99]],
        [6, [13, 14, 15, 35]],
        [8, [26, 27, 31, 32]]  # separate them out from HWBin4
    ],
    [
        [3, [1, 2, 3]],
        [1, [63, 64, 65, 89, 90, 94]],
        [2, [53, 54, 73, 74]],
        [4, [23, 24, 25, 26, 27, 31, 32, 36, 56, 57, 58, 75, 29, 30, 33, 34, 36, 39, 40]],
        [5, [5, 6, 7, 8, 9, 12, 93, 96, 98, 99]],
        [6, [13, 14, 15, 46, 47, 48, 51, 60]]
        # ,[8, [29, 30, 33, 34, 36, 39, 40]] # put them back to HWBin4
    ]
]

bin_definition_list = [
    [('PCLK_O/S', 5, 5),
     ('HSYNC_O/S', 5, 5),
     ('VSYNC_O/S', 5, 5),
     ('D9_O/S', 5, 5),
     ('D8_O/S', 5, 5),
     ('D7_O/S', 5, 5),
     ('D6_O/S', 5, 5),
     ('D5_O/S', 5, 5),
     ('D4_O/S', 5, 5),
     ('D3_O/S', 5, 5),
     ('D2_O/S', 5, 5),
     ('D1_O/S', 5, 5),
     ('D0_O/S', 5, 5),
     ('SCL_O/S', 5, 5),
     ('SDA_O/S', 5, 5),
     ('RSTB_O/S', 5, 5),
     ('PWDN_O/S', 5, 5),
     ('DVDD_O/S', 5, 5),
     ('VRamp_O/S', 5, 5),
     ('VH_O/S', 5, 5),
     ('VN1_O/S', 5, 5),
     ('EXCLK_O/S', 5, 5),
     ('PCLK_Leakage/iiL', 6, 5),
     ('HSYNC_Leakage/iiL', 6, 5),
     ('VSYNC_Leakage/iiL', 6, 5),
     ('D9_Leakage/iiL', 6, 5),
     ('D8_Leakage/iiL', 6, 5),
     ('D7_Leakage/iiL', 6, 5),
     ('D6_Leakage/iiL', 6, 5),
     ('D5_Leakage/iiL', 6, 5),
     ('D4_Leakage/iiL', 6, 5),
     ('D3_Leakage/iiL', 6, 5),
     ('D2_Leakage/iiL', 6, 5),
     ('D1_Leakage/iiL', 6, 5),
     ('D0_Leakage/iiL', 6, 5),
     ('SCL_Leakage/iiL', 6, 5),
     ('SDA_Leakage/iiL', 6, 5),
     ('RSTB_Leakage/iiL', 6, 5),
     ('PWDN_Leakage/iiL', 6, 5),
     ('EXCLK_Leakage/iiL', 6, 5),
     ('PCLK_Leakage/iiH', 6, 5),
     ('HSYNC_Leakage/iiH', 6, 5),
     ('VSYNC_Leakage/iiH', 6, 5),
     ('D9_Leakage/iiH', 6, 5),
     ('D8_Leakage/iiH', 6, 5),
     ('D7_Leakage/iiH', 6, 5),
     ('D6_Leakage/iiH', 6, 5),
     ('D5_Leakage/iiH', 6, 5),
     ('D4_Leakage/iiH', 6, 5),
     ('D3_Leakage/iiH', 6, 5),
     ('D2_Leakage/iiH', 6, 5),
     ('D1_Leakage/iiH', 6, 5),
     ('D0_Leakage/iiH', 6, 5),
     ('SCL_Leakage/iiH', 6, 5),
     ('SDA_Leakage/iiH', 6, 5),
     ('RSTB_Leakage/iiH', 6, 5),
     ('PWDN_Leakage/iiH', 6, 5),
     ('EXCLK_Leakage/iiH', 6, 5),
     ('iic_test', 7, 5),
     ('DVDD_voltage', 9, 5),
     ('VH_voltage', 9, 5),
     ('VN1_voltage', 9, 5),
     ('Active_AVDD', 12, 5),
     ('Active_DOVDD', 12, 5),
     ('PWDN_AVDD', 8, 5),
     ('PWDN_DOVDD', 8, 5),
     ('PWDN_Total', 8, 5),
     ('PLCK_Freq', 9, 5),
     ('BLC_R', 7, 5),
     ('BLC_Gr', 7, 5),
     ('BLC_Gb', 7, 5),
     ('BLC_B', 7, 5),
     ('BK_ImageCapture', 98, 5),
     ('BK_DeadRowExBPix_R', 15, 6),
     ('BK_DeadRowExBPix_Gr', 15, 6),
     ('BK_DeadRowExBPix_Gb', 15, 6),
     ('BK_DeadRowExBPix_B', 15, 6),
     ('BK_DeadColExBPix_R', 14, 6),
     ('BK_DeadColExBPix_Gr', 14, 6),
     ('BK_DeadColExBPix_Gb', 14, 6),
     ('BK_DeadColExBPix_B', 14, 6),
     ('BK_Mean_R', 13, 6),
     ('BK_Mean_Gr', 13, 6),
     ('BK_Mean_Gb', 13, 6),
     ('BK_Mean_B', 13, 6),
     ('BK_StdDEV_R', 13, 6),
     ('BK_StdDEV_Gr', 13, 6),
     ('BK_StdDEV_Gb', 13, 6),
     ('BK_StdDEV_B', 13, 6),
     ('LT_ImageCapture', 99, 5),
     ('LT_DRow_R', 25, 4),
     ('LT_DRow_Gr', 25, 4),
     ('LT_DRow_Gb', 25, 4),
     ('LT_DRow_B', 25, 4),
     ('LT_DCol_R', 24, 4),
     ('LT_DCol_Gr', 24, 4),
     ('LT_DCol_Gb', 24, 4),
     ('LT_DCol_B', 24, 4),
     ('LT_DRow_Color', 25, 4),
     ('LT_DCol_Color', 24, 4),
     ('LT_Mean_R', 23, 4),
     ('LT_Mean_Gr', 23, 4),
     ('LT_Mean_Gb', 23, 4),
     ('LT_Mean_B', 23, 4),
     ('LT_StdDEV_R', 23, 4),
     ('LT_StdDEV_Gr', 23, 4),
     ('LT_StdDEV_Gb', 23, 4),
     ('LT_StdDEV_B', 23, 4),
     ('LT_RI_R', 23, 4),
     ('LT_RI_Gr', 23, 4),
     ('LT_RI_Gb', 23, 4),
     ('LT_RI_B', 23, 4),
     ('LT_Ratio_GrR', 23, 4),
     ('LT_Ratio_GbR', 23, 4),
     ('LT_Ratio_GrB', 23, 4),
     ('LT_Ratio_GbB', 23, 4),
     ('LT_Ratio_GbGr', 23, 4),
     ('LT_LostBit', 23, 4),
     ('LT_LostBitSNR_SumDIFF_R', 23, 4),
     ('LT_LostBitSNR_SumDIFF_Gr', 23, 4),
     ('LT_LostBitSNR_SumDIFF_Gb', 23, 4),
     ('LT_LostBitSNR_SumDIFF_B', 23, 4),
     ('LB_LT_ImageCapture', 99, 5),
     ('LB_LT_Mean_R', 23, 4),
     ('LB_LT_Mean_Gr', 23, 4),
     ('LB_LT_Mean_Gb', 23, 4),
     ('LB_LT_Mean_B', 23, 4),
     ('LB_LT_LostBit', 23, 4),
     ('LB_LT_LostBitSNR_SumDIFF_R', 23, 4),
     ('LB_LT_LostBitSNR_SumDIFF_Gr', 23, 4),
     ('LB_LT_LostBitSNR_SumDIFF_Gb', 23, 4),
     ('LB_LT_LostBitSNR_SumDIFF_B', 23, 4),
     ('FW_LT_ImageCapture', 99, 5),
     ('FW_LT_DRow_R', 36, 4),
     ('FW_LT_DRow_Gr', 36, 4),
     ('FW_LT_DRow_Gb', 36, 4),
     ('FW_LT_DRow_B', 36, 4),
     ('FW_LT_DCol_R', 36, 4),
     ('FW_LT_DCol_Gr', 36, 4),
     ('FW_LT_DCol_Gb', 36, 4),
     ('FW_LT_DCol_B', 36, 4),
     ('FW_LT_DRow_Color', 36, 4),
     ('FW_LT_DCol_Color', 36, 4),
     ('FW_LT_Mean_R', 36, 4),
     ('FW_LT_Mean_Gr', 36, 4),
     ('FW_LT_Mean_Gb', 36, 4),
     ('FW_LT_Mean_B', 36, 4),
     ('FW_LT_StdDEV_R', 36, 4),
     ('FW_LT_StdDEV_Gr', 36, 4),
     ('FW_LT_StdDEV_Gb', 36, 4),
     ('FW_LT_StdDEV_B', 36, 4),
     ('FW_LT_RI_R', 36, 4),
     ('FW_LT_RI_Gr', 36, 4),
     ('FW_LT_RI_Gb', 36, 4),
     ('FW_LT_RI_B', 36, 4),
     ('FW_LT_Ratio_GrR', 36, 4),
     ('FW_LT_Ratio_GbR', 36, 4),
     ('FW_LT_Ratio_GrB', 36, 4),
     ('FW_LT_Ratio_GbB', 36, 4),
     ('FW_LT_Ratio_GbGr', 36, 4),
     ('LT_CornerLine', 26, 8),  # 4
     ('LT_ScratchLine', 26, 8),  # 4
     ('LT_Blemish', 31, 8),  # 4
     ('LT_LineStripe', 27, 8),  # 4
     ('LT_Particle', 32, 8),  # 4
     ('BK_Cluster2', 30, 4),
     ('LT_Cluster2', 30, 4),
     ('BK_Cluster1', 29, 4),
     ('LT_Cluster1', 29, 4),
     ('WP_Count', 35, 6),
     ('BK_Cluster3GrGb', 39, 4),
     ('LT_Cluster3GrGb', 40, 4),
     ('BK_Cluster3SubtractGrGb', 33, 4),
     ('LT_Cluster3SubtractGrGb', 34, 4),
     ('LB_BK_DeadRowExBPix_R', 45, 2),
     ('LB_BK_DeadRowExBPix_Gr', 45, 2),
     ('LB_BK_DeadRowExBPix_Gb', 45, 2),
     ('LB_BK_DeadRowExBPix_B', 45, 2),
     ('LB_BK_DeadColExBPix_R', 44, 2),
     ('LB_BK_DeadColExBPix_Gr', 44, 2),
     ('LB_BK_DeadColExBPix_Gb', 44, 2),
     ('LB_BK_DeadColExBPix_B', 44, 2),
     ('SR_LT_ImageCapture', 96, 5),
     ('SR_LT_DRow_R', 55, 2),
     ('SR_LT_DRow_Gr', 55, 2),
     ('SR_LT_DRow_Gb', 55, 2),
     ('SR_LT_DRow_B', 55, 2),
     ('SR_LT_DCol_R', 54, 2),
     ('SR_LT_DCol_Gr', 54, 2),
     ('SR_LT_DCol_Gb', 54, 2),
     ('SR_LT_DCol_B', 54, 2),
     ('SR_LT_DRow_Color', 55, 2),
     ('SR_LT_DCol_Color', 54, 2),
     ('SR_LT_Mean_R', 53, 2),
     ('SR_LT_Mean_Gr', 53, 2),
     ('SR_LT_Mean_Gb', 53, 2),
     ('SR_LT_Mean_B', 53, 2),
     ('SR_LT_StdDEV_R', 53, 2),
     ('SR_LT_StdDEV_Gr', 53, 2),
     ('SR_LT_StdDEV_Gb', 53, 2),
     ('SR_LT_StdDEV_B', 53, 2),
     ('SR_LT_RI_R', 53, 2),
     ('SR_LT_RI_Gr', 53, 2),
     ('SR_LT_RI_Gb', 53, 2),
     ('SR_LT_RI_B', 53, 2),
     ('SR_LT_Ratio_GrR', 53, 2),
     ('SR_LT_Ratio_GbR', 53, 2),
     ('SR_LT_Ratio_GrB', 53, 2),
     ('SR_LT_Ratio_GbB', 53, 2),
     ('SR_LT_Ratio_GbGr', 53, 2),
     ('SR_LT_LostBit', 53, 2),
     ('SR_BK_ImageCapture', 96, 5),
     ('SR_BK_DeadRowExBPix_R', 42, 2),
     ('SR_BK_DeadRowExBPix_Gr', 42, 2),
     ('SR_BK_DeadRowExBPix_Gb', 42, 2),
     ('SR_BK_DeadRowExBPix_B', 42, 2),
     ('SR_BK_DeadColExBPix_R', 41, 2),
     ('SR_BK_DeadColExBPix_Gr', 41, 2),
     ('SR_BK_DeadColExBPix_Gb', 41, 2),
     ('SR_BK_DeadColExBPix_B', 41, 2),
     ('SR_BK_Mean_R', 43, 2),
     ('SR_BK_Mean_Gr', 43, 2),
     ('SR_BK_Mean_Gb', 43, 2),
     ('SR_BK_Mean_B', 43, 2),
     ('SR_BK_StdDEV_R', 43, 2),
     ('SR_BK_StdDEV_Gr', 43, 2),
     ('SR_BK_StdDEV_Gb', 43, 2),
     ('SR_BK_StdDEV_B', 43, 2),
     # ('Diffuser2_LT_ImageCapture', 99, 5),
     # ('Diffuser2_LT_WeakLineRow_R', 72, 4),
     # ('Diffuser2_LT_WeakLineRow_Gr', 72, 4),
     # ('Diffuser2_LT_WeakLineRow_Gb', 72, 4),
     # ('Diffuser2_LT_WeakLineRow_B', 72, 4),
     # ('Diffuser2_LT_WeakLineCol_R', 71, 4),
     # ('Diffuser2_LT_WeakLineCol_Gr', 71, 4),
     # ('Diffuser2_LT_WeakLineCol_Gb', 71, 4),
     # ('Diffuser2_LT_WeakLineCol_B', 71, 4),
     ('Binning', 2, 1),
     ('All Pass', 1, 1)
     ],
    [('VSYNC_O/S', 5, 5),
     ('HSYNC_O/S', 5, 5),
     ('PCLK_O/S', 5, 5),
     ('EXCLK_O/S', 5, 5),
     ('RSTB_O/S', 5, 5),
     ('PWDN_O/S', 5, 5),
     ('SDA_O/S', 5, 5),
     ('SCL_O/S', 5, 5),
     ('D0_O/S', 5, 5),
     ('D1_O/S', 5, 5),
     ('D2_O/S', 5, 5),
     ('D3_O/S', 5, 5),
     ('D4_O/S', 5, 5),
     ('D5_O/S', 5, 5),
     ('D6_O/S', 5, 5),
     ('D7_O/S', 5, 5),
     ('D8_O/S', 5, 5),
     ('D9_O/S', 5, 5),
     ('MCP_O/S', 5, 5),
     ('MCN_O/S', 5, 5),
     ('MDP0_O/S', 5, 5),
     ('MDN0_O/S', 5, 5),
     ('MDP1_O/S', 5, 5),
     ('MDN1_O/S', 5, 5),
     ('AVDD_O/S', 5, 5),
     ('DOVDD_O/S', 5, 5),
     ('VRamp_O/S', 5, 5),
     ('VH_O/S', 5, 5),
     ('VN1_O/S', 5, 5),

     ('VSYNC_Leakage/iiL', 6, 5),
     ('HSYNC_Leakage/iiL', 6, 5),
     ('PCLK_Leakage/iiL', 6, 5),
     ('EXCLK_Leakage/iiL', 6, 5),
     ('RSTB_Leakage/iiL', 6, 5),
     ('PWDN_Leakage/iiL', 6, 5),
     ('SDA_Leakage/iiL', 6, 5),
     ('SCL_Leakage/iiL', 6, 5),
     ('D0_Leakage/iiL', 6, 5),
     ('D1_Leakage/iiL', 6, 5),
     ('D2_Leakage/iiL', 6, 5),
     ('D4_Leakage/iiL', 6, 5),
     ('D5_Leakage/iiL', 6, 5),
     ('D3_Leakage/iiL', 6, 5),
     ('D6_Leakage/iiL', 6, 5),
     ('D7_Leakage/iiL', 6, 5),
     ('D8_Leakage/iiL', 6, 5),
     ('D9_Leakage/iiL', 6, 5),
     ('MCP_Leakage/iiL', 6, 5),
     ('MCN_Leakage/iiL', 6, 5),
     ('MDP0_Leakage/iiL', 6, 5),
     ('MDN0_Leakage/iiL', 6, 5),
     ('MDP1_Leakage/iiL', 6, 5),
     ('MDN1_Leakage/iiL', 6, 5),

     ('VSYNC_Leakage/iiH', 6, 5),
     ('HSYNC_Leakage/iiH', 6, 5),
     ('PCLK_Leakage/iiH', 6, 5),
     ('EXCLK_Leakage/iiH', 6, 5),
     ('RSTB_Leakage/iiH', 6, 5),
     ('PWDN_Leakage/iiH', 6, 5),
     ('SDA_Leakage/iiH', 6, 5),
     ('SCL_Leakage/iiH', 6, 5),
     ('D0_Leakage/iiH', 6, 5),
     ('D1_Leakage/iiH', 6, 5),
     ('D2_Leakage/iiH', 6, 5),
     ('D4_Leakage/iiH', 6, 5),
     ('D5_Leakage/iiH', 6, 5),
     ('D3_Leakage/iiH', 6, 5),
     ('D6_Leakage/iiH', 6, 5),
     ('D7_Leakage/iiH', 6, 5),
     ('D8_Leakage/iiH', 6, 5),
     ('D9_Leakage/iiH', 6, 5),
     ('MCP_Leakage/iiH', 6, 5),
     ('MCN_Leakage/iiH', 6, 5),
     ('MDP0_Leakage/iiH', 6, 5),
     ('MDN0_Leakage/iiH', 6, 5),
     ('MDP1_Leakage/iiH', 6, 5),
     ('MDN1_Leakage/iiH', 6, 5),

     ('iic_test', 7, 5),
     ('DVDD_voltage', 9, 5),
     ('VH_voltage', 9, 5),
     ('VN1_voltage', 9, 5),
     ('Active_AVDD', 12, 5),
     ('Active_DOVDD', 12, 5),
     ('PWDN_AVDD', 8, 5),
     ('PWDN_DOVDD', 8, 5),
     ('PWDN_Total', 8, 5),

     ('BLC_R', 7, 5),
     ('BLC_Gr', 7, 5),
     ('BLC_Gb', 7, 5),
     ('BLC_B', 7, 5),
     ('DVP27M30F_BK_Cap', 98, 5),
     ('BK_DeadRowExBPix_R', 15, 6),
     ('BK_DeadRowExBPix_Gr', 15, 6),
     ('BK_DeadRowExBPix_Gb', 15, 6),
     ('BK_DeadRowExBPix_B', 15, 6),
     ('BK_DeadColExBPix_R', 14, 6),
     ('BK_DeadColExBPix_Gr', 14, 6),
     ('BK_DeadColExBPix_Gb', 14, 6),
     ('BK_DeadColExBPix_B', 14, 6),
     ('BK_MixDCol_VfpnQty_R', 14, 6),
     ('BK_MixDCol_VfpnQty_Gr', 14, 6),
     ('BK_MixDCol_VfpnQty_Gb', 14, 6),
     ('BK_MixDCol_VfpnQty_B', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue0_R', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue0_Gr', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue0_Gb', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue0_B', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue1_R', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue1_Gr', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue1_Gb', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue1_B', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue2_R', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue2_Gr', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue2_Gb', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue2_B', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue3_R', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue3_Gr', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue3_Gb', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue3_B', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue4_R', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue4_Gr', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue4_Gb', 14, 6),
     ('BK_MixDCol_VFPN_MaxValue4_B', 14, 6),
     ('BK_Mean_R', 13, 6),
     ('BK_Mean_Gr', 13, 6),
     ('BK_Mean_Gb', 13, 6),
     ('BK_Mean_B', 13, 6),
     ('BK_StdDEV_R', 13, 6),
     ('BK_StdDEV_Gr', 13, 6),
     ('BK_StdDEV_Gb', 13, 6),
     ('BK_StdDEV_B', 13, 6),

     ('DVP27M30F_LT_Cap', 99, 5),
     ('PLCK_Freq', 93, 5),
     ('LT_DRow_R', 25, 4),
     ('LT_DRow_Gr', 25, 4),
     ('LT_DRow_Gb', 25, 4),
     ('LT_DRow_B', 25, 4),
     ('LT_DCol_R', 24, 4),
     ('LT_DCol_Gr', 24, 4),
     ('LT_DCol_Gb', 24, 4),
     ('LT_DCol_B', 24, 4),
     ('LT_DRow_Color', 25, 4),
     ('LT_DCol_Color', 24, 4),
     ('LT_WeakLineRow_R', 25, 4),
     ('LT_WeakLineRow_Gr', 25, 4),
     ('LT_WeakLineRow_Gb', 25, 4),
     ('LT_WeakLineRow_B', 25, 4),
     ('LT_WeakLineCol_R', 24, 4),
     ('LT_WeakLineCol_Gr', 24, 4),
     ('LT_WeakLineCol_Gb', 24, 4),
     ('LT_WeakLineCol_B', 24, 4),
     ('LT_Mean_R', 23, 4),
     ('LT_Mean_Gr', 23, 4),
     ('LT_Mean_Gb', 23, 4),
     ('LT_Mean_B', 23, 4),
     ('LT_StdDEV_R', 23, 4),
     ('LT_StdDEV_Gr', 23, 4),
     ('LT_StdDEV_Gb', 23, 4),
     ('LT_StdDEV_B', 23, 4),
     ('LT_RI_R', 23, 4),
     ('LT_RI_Gr', 23, 4),
     ('LT_RI_Gb', 23, 4),
     ('LT_RI_B', 23, 4),
     ('LT_Ratio_GrR', 23, 4),
     ('LT_Ratio_GbR', 23, 4),
     ('LT_Ratio_GrB', 23, 4),
     ('LT_Ratio_GbB', 23, 4),
     ('LT_Ratio_GbGr', 23, 4),
     ('LT_LostBit', 23, 4),
     ('LT_LostBitSNR_SumDIFF_R', 23, 4),
     ('LT_LostBitSNR_SumDIFF_Gr', 23, 4),
     ('LT_LostBitSNR_SumDIFF_Gb', 23, 4),
     ('LT_LostBitSNR_SumDIFF_B', 23, 4),

     ('DVP27M30F_LBIT_Cap', 99, 5),
     ('LBIT_LT_Mean_R', 23, 4),
     ('LBIT_LT_Mean_Gr', 23, 4),
     ('LBIT_LT_Mean_Gb', 23, 4),
     ('LBIT_LT_Mean_B', 23, 4),
     ('LBIT_LT_LostBit', 23, 4),
     ('LBIT_LT_LostBitSNR_SumDIFF_R', 23, 4),
     ('LBIT_LT_LostBitSNR_SumDIFF_Gr', 23, 4),
     ('LBIT_LT_LostBitSNR_SumDIFF_Gb', 23, 4),
     ('LBIT_LT_LostBitSNR_SumDIFF_B', 23, 4),

     ('DVP27M30F_FW_Cap', 99, 5),
     ('FW_LT_DRow_R', 36, 4),
     ('FW_LT_DRow_Gr', 36, 4),
     ('FW_LT_DRow_Gb', 36, 4),
     ('FW_LT_DRow_B', 36, 4),
     ('FW_LT_DCol_R', 36, 4),
     ('FW_LT_DCol_Gr', 36, 4),
     ('FW_LT_DCol_Gb', 36, 4),
     ('FW_LT_DCol_B', 36, 4),
     ('FW_LT_DRow_Color', 36, 4),
     ('FW_LT_DCol_Color', 36, 4),
     ('FW_LT_Mean_R', 36, 4),
     ('FW_LT_Mean_Gr', 36, 4),
     ('FW_LT_Mean_Gb', 36, 4),
     ('FW_LT_Mean_B', 36, 4),
     ('FW_LT_StdDEV_R', 36, 4),
     ('FW_LT_StdDEV_Gr', 36, 4),
     ('FW_LT_StdDEV_Gb', 36, 4),
     ('FW_LT_StdDEV_B', 36, 4),
     ('FW_LT_RI_R', 36, 4),
     ('FW_LT_RI_Gr', 36, 4),
     ('FW_LT_RI_Gb', 36, 4),
     ('FW_LT_RI_B', 36, 4),
     ('FW_LT_Ratio_GrR', 36, 4),
     ('FW_LT_Ratio_GbR', 36, 4),
     ('FW_LT_Ratio_GrB', 36, 4),
     ('FW_LT_Ratio_GbB', 36, 4),
     ('FW_LT_Ratio_GbGr', 36, 4),
     ('FW_LT_LostBit', 36, 4),

     ('DVP27M30F_BSun_Cap', 96, 5),
     ('BSun_BK_DeadRowExBPix_R', 48, 6),
     ('BSun_BK_DeadRowExBPix_Gr', 48, 6),
     ('BSun_BK_DeadRowExBPix_Gb', 48, 6),
     ('BSun_BK_DeadRowExBPix_B', 48, 6),
     ('BSun_BK_DeadColExBPix_R', 47, 6),
     ('BSun_BK_DeadColExBPix_Gr', 47, 6),
     ('BSun_BK_DeadColExBPix_Gb', 47, 6),
     ('BSun_BK_DeadColExBPix_B', 47, 6),
     ('BSun_BK_Mean_R', 46, 6),
     ('BSun_BK_Mean_Gr', 46, 6),
     ('BSun_BK_Mean_Gb', 46, 6),
     ('BSun_BK_Mean_B', 46, 6),
     ('BSun_BK_StdDEV_R', 46, 6),
     ('BSun_BK_StdDEV_Gr', 46, 6),
     ('BSun_BK_StdDEV_Gb', 46, 6),
     ('BSun_BK_StdDEV_B', 46, 6),

     ('DVP27M30F_LMFlip_Cap', 96, 5),
     ('LMFlip_LT_DRow_R', 58, 4),
     ('LMFlip_LT_DRow_Gr', 58, 4),
     ('LMFlip_LT_DRow_Gb', 58, 4),
     ('LMFlip_LT_DRow_B', 58, 4),
     ('LMFlip_LT_DCol_R', 57, 4),
     ('LMFlip_LT_DCol_Gr', 57, 4),
     ('LMFlip_LT_DCol_Gb', 57, 4),
     ('LMFlip_LT_DCol_B', 57, 4),
     ('LMFlip_LT_DRow_Color', 58, 4),
     ('LMFlip_LT_DCol_Color', 57, 4),
     ('LMFlip_LT_WeakLineRow_R', 58, 4),
     ('LMFlip_LT_WeakLineRow_Gr', 58, 4),
     ('LMFlip_LT_WeakLineRow_Gb', 58, 4),
     ('LMFlip_LT_WeakLineRow_B', 58, 4),
     ('LMFlip_LT_WeakLineCol_R', 57, 4),
     ('LMFlip_LT_WeakLineCol_Gr', 57, 4),
     ('LMFlip_LT_WeakLineCol_Gb', 57, 4),
     ('LMFlip_LT_WeakLineCol_B', 57, 4),
     ('LMFlip_LT_Mean_R', 56, 4),
     ('LMFlip_LT_Mean_Gr', 56, 4),
     ('LMFlip_LT_Mean_Gb', 56, 4),
     ('LMFlip_LT_Mean_B', 56, 4),
     ('LMFlip_LT_StdDEV_R', 56, 4),
     ('LMFlip_LT_StdDEV_Gr', 56, 4),
     ('LMFlip_LT_StdDEV_Gb', 56, 4),
     ('LMFlip_LT_StdDEV_B', 56, 4),
     ('LMFlip_LT_RI_R', 56, 4),
     ('LMFlip_LT_RI_Gr', 56, 4),
     ('LMFlip_LT_RI_Gb', 56, 4),
     ('LMFlip_LT_RI_B', 56, 4),
     ('LMFlip_LT_Ratio_GrR', 56, 4),
     ('LMFlip_LT_Ratio_GbR', 56, 4),
     ('LMFlip_LT_Ratio_GrB', 56, 4),
     ('LMFlip_LT_Ratio_GbB', 56, 4),
     ('LMFlip_LT_Ratio_GbGr', 56, 4),
     ('LMFlip_LT_LostBit', 56, 4),
     ('LMFlip_LT_LostBitSNR_SumDIFF_R', 56, 4),
     ('LMFlip_LT_LostBitSNR_SumDIFF_Gr', 56, 4),
     ('LMFlip_LT_LostBitSNR_SumDIFF_Gb', 56, 4),
     ('LMFlip_LT_LostBitSNR_SumDIFF_B', 56, 4),

     ('LT_CornerLine', 26, 4),
     ('LT_ScratchLine', 26, 4),
     ('LT_Blemish', 31, 4),
     ('LT_LineStripe', 27, 4),
     ('LT_Particle', 32, 4),
     ('BK_Cluster2', 30, 4),  # 4/8
     ('LT_Cluster2', 30, 4),  # 4/8
     ('BK_Cluster1', 29, 4),  # 4/8
     ('LT_Cluster1', 29, 4),  # 4/8
     ('BK_Cluster3GrGb', 39, 4),  # 4/8
     ('LT_Cluster3GrGb', 40, 4),  # 4/8
     ('BK_Cluster3SubtractGrGb', 33, 4),  # 4/8
     ('LT_Cluster3SubtractGrGb', 34, 4),  # 4/8
     ('WP_Count', 35, 4),  # 6/8

     ('BK_Z1_BT_DP_R', 60, 6),
     ('BK_Z1_BT_DP_Gr', 60, 6),
     ('BK_Z1_BT_DP_Gb', 60, 6),
     ('BK_Z1_BT_DP_B', 60, 6),
     ('BK_Z2_BT_DP_R', 60, 6),
     ('BK_Z2_BT_DP_Gr', 60, 6),
     ('BK_Z2_BT_DP_Gb', 60, 6),
     ('BK_Z2_BT_DP_B', 60, 6),
     ('BK_Z1_BT_WP_R', 60, 6),
     ('BK_Z1_BT_WP_Gr', 60, 6),
     ('BK_Z1_BT_WP_Gb', 60, 6),
     ('BK_Z1_BT_WP_B', 60, 6),
     ('BK_Z2_BT_WP_R', 60, 6),
     ('BK_Z2_BT_WP_Gr', 60, 6),
     ('BK_Z2_BT_WP_Gb', 60, 6),
     ('BK_Z2_BT_WP_B', 60, 6),
     ('LT_Z1_BT_DP_R', 60, 6),
     ('LT_Z1_BT_DP_Gr', 60, 6),
     ('LT_Z1_BT_DP_Gb', 60, 6),
     ('LT_Z1_BT_DP_B', 60, 6),
     ('LT_Z2_BT_DP_R', 60, 6),
     ('LT_Z2_BT_DP_Gr', 60, 6),
     ('LT_Z2_BT_DP_Gb', 60, 6),
     ('LT_Z2_BT_DP_B', 60, 6),
     ('LT_Z1_BT_WP_R', 60, 6),
     ('LT_Z1_BT_WP_Gr', 60, 6),
     ('LT_Z1_BT_WP_Gb', 60, 6),
     ('LT_Z1_BT_WP_B', 60, 6),
     ('LT_Z2_BT_WP_R', 60, 6),
     ('LT_Z2_BT_WP_Gr', 60, 6),
     ('LT_Z2_BT_WP_Gb', 60, 6),
     ('LT_Z2_BT_WP_B', 60, 6),
     ('LT_Z1_DK_WP_R', 60, 6),
     ('LT_Z1_DK_WP_Gr', 60, 6),
     ('LT_Z1_DK_WP_Gb', 60, 6),
     ('LT_Z1_DK_WP_B', 60, 6),
     ('LT_Z2_DK_WP_R', 60, 6),
     ('LT_Z2_DK_WP_Gr', 60, 6),
     ('LT_Z2_DK_WP_Gb', 60, 6),
     ('LT_Z2_DK_WP_B', 60, 6),
     ('LT_Z1_DK_DP_R', 60, 6),
     ('LT_Z1_DK_DP_Gr', 60, 6),
     ('LT_Z1_DK_DP_Gb', 60, 6),
     ('LT_Z1_DK_DP_B', 60, 6),
     ('LT_Z2_DK_DP_R', 60, 6),
     ('LT_Z2_DK_DP_Gr', 60, 6),
     ('LT_Z2_DK_DP_Gb', 60, 6),
     ('LT_Z2_DK_DP_B', 60, 6),
     ('BK_Z1_BT_DP', 60, 6),
     ('BK_Z2_BT_DP', 60, 6),
     ('BK_Z1_BT_WP', 60, 6),
     ('BK_Z2_BT_WP', 60, 6),
     ('LT_Z1_BT_DP', 60, 6),
     ('LT_Z2_BT_DP', 60, 6),
     ('LT_Z1_BT_WP', 60, 6),
     ('LT_Z2_BT_WP', 60, 6),
     ('LT_Z1_DK_DP', 60, 6),
     ('LT_Z2_DK_DP', 60, 6),
     ('LT_Z1_DK_WP', 60, 6),
     ('LT_Z2_DK_WP', 60, 6),

     ('DVP27M30F_BK32X_Cap', 98, 5),
     ('BK32X_BK_BadPixel_Area', 75, 4),
     ('BK32X_BK_MixDCol_DashQty_R', 51, 6),
     ('BK32X_BK_MixDCol_DashQty_Gr', 51, 6),
     ('BK32X_BK_MixDCol_DashQty_Gb', 51, 6),
     ('BK32X_BK_MixDCol_DashQty_B', 51, 6),
     ('BK32X_SP_BK_MixDCol_DashQty_R', 54, 2),
     ('BK32X_SP_BK_MixDCol_DashQty_Gr', 54, 2),
     ('BK32X_SP_BK_MixDCol_DashQty_Gb', 54, 2),
     ('BK32X_SP_BK_MixDCol_DashQty_B', 54, 2),
     ('BK32X_BK_MixDCol_DASH_DeltaAvg_R', 54, 2),
     ('BK32X_BK_MixDCol_DASH_DeltaAvg_Gr', 54, 2),
     ('BK32X_BK_MixDCol_DASH_DeltaAvg_Gb', 54, 2),
     ('BK32X_BK_MixDCol_DASH_DeltaAvg_B', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue0_R', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue0_Gr', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue0_Gb', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue0_B', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue1_R', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue1_Gr', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue1_Gb', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue1_B', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue2_R', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue2_Gr', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue2_Gb', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue2_B', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue3_R', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue3_Gr', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue3_Gb', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue3_B', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue4_R', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue4_Gr', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue4_Gb', 54, 2),
     ('BK32X_BK_MixDCol_DASH_MaxValue4_B', 54, 2),
     ('BK32X_BK_Mean_R', 53, 2),
     ('BK32X_BK_Mean_Gr', 53, 2),
     ('BK32X_BK_Mean_Gb', 53, 2),
     ('BK32X_BK_Mean_B', 53, 2),
     ('BK32X_BK_StdDEV_R', 53, 2),
     ('BK32X_BK_StdDEV_Gr', 53, 2),
     ('BK32X_BK_StdDEV_Gb', 53, 2),
     ('BK32X_BK_StdDEV_B', 53, 2),
     ('BK_Cluster3_2', 73, 2),
     ('LT_Cluster3_2', 74, 2),

     ('MIPI2L24M30F_WK1_Cap', 89, 1),
     ('MIPI_One_W1_FixedPattern', 94, 1),
     # ('MIPI2L24M30F_WK1_Protocol1', 94, 1),
     # ('MIPI2L24M30F_WK1_Protocol2', 94, 1),
     # ('MIPI2L24M30F_WK1_Protocol3', 94, 1),
     # ('MIPI2L24M30F_WK1_Skew', 94, 1),
     # ('MIPI2L24M30F_WK1_ErrCnt', 94, 1),

     ('MIPI2L24M30F_LT_Cap', 90, 1),
     # ('MIPI2L24M30F_LT_Protocol1', 94, 1),
     # ('MIPI2L24M30F_LT_Protocol2', 94, 1),
     # ('MIPI2L24M30F_LT_Protocol3', 94, 1),
     # ('MIPI2L24M30F_LT_Skew', 94, 1),
     ('MIPI_LT_DRow_R', 65, 1),
     ('MIPI_LT_DRow_Gr', 65, 1),
     ('MIPI_LT_DRow_Gb', 65, 1),
     ('MIPI_LT_DRow_B', 65, 1),
     ('MIPI_LT_DCol_R', 64, 1),
     ('MIPI_LT_DCol_Gr', 64, 1),
     ('MIPI_LT_DCol_Gb', 64, 1),
     ('MIPI_LT_DCol_B', 64, 1),
     ('MIPI_LT_DRow_Color', 65, 1),
     ('MIPI_LT_DCol_Color', 64, 1),
     ('MIPI_LT_WeakLineRow_R', 65, 1),
     ('MIPI_LT_WeakLineRow_Gr', 65, 1),
     ('MIPI_LT_WeakLineRow_Gb', 65, 1),
     ('MIPI_LT_WeakLineRow_B', 65, 1),
     ('MIPI_LT_WeakLineCol_R', 64, 1),
     ('MIPI_LT_WeakLineCol_Gr', 64, 1),
     ('MIPI_LT_WeakLineCol_Gb', 64, 1),
     ('MIPI_LT_WeakLineCol_B', 64, 1),
     ('MIPI_LT_Mean_R', 63, 1),
     ('MIPI_LT_Mean_Gr', 63, 1),
     ('MIPI_LT_Mean_Gb', 63, 1),
     ('MIPI_LT_Mean_B', 63, 1),
     ('MIPI_LT_StdDEV_R', 63, 1),
     ('MIPI_LT_StdDEV_Gr', 63, 1),
     ('MIPI_LT_StdDEV_Gb', 63, 1),
     ('MIPI_LT_StdDEV_B', 63, 1),
     ('MIPI_LT_RI_R', 63, 1),
     ('MIPI_LT_RI_Gr', 63, 1),
     ('MIPI_LT_RI_Gb', 63, 1),
     ('MIPI_LT_RI_B', 63, 1),
     ('MIPI_LT_Ratio_GrR', 63, 1),
     ('MIPI_LT_Ratio_GbR', 63, 1),
     ('MIPI_LT_Ratio_GrB', 63, 1),
     ('MIPI_LT_Ratio_GbB', 63, 1),
     ('MIPI_LT_Ratio_GbGr', 63, 1),
     ('MIPI_LT_LostBit', 63, 1),
     ('MIPI_LT_LostBitSNR_SumDIFF_R', 63, 1),
     ('MIPI_LT_LostBitSNR_SumDIFF_Gr', 63, 1),
     ('MIPI_LT_LostBitSNR_SumDIFF_Gb', 63, 1),
     ('MIPI_LT_LostBitSNR_SumDIFF_B', 63, 1),

     ('MIPI2L24M30F_LBIT_Cap', 90, 1),
     ('MIPI_LBIT_LT_Mean_R', 63, 1),
     ('MIPI_LBIT_LT_Mean_Gr', 63, 1),
     ('MIPI_LBIT_LT_Mean_Gb', 63, 1),
     ('MIPI_LBIT_LT_Mean_B', 63, 1),
     ('MIPI_LBIT_LT_LostBit', 63, 1),
     ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_R', 63, 1),
     ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_Gr', 63, 1),
     ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_Gb', 63, 1),
     ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_B', 63, 1),

     ('Binning', 2, 3),
     ('All Pass', 1, 3)
     ]
]

golden_data_list = [
    [('PCLK_O/S', -0.38, -0.5),
     ('HSYNC_O/S', -0.38, -0.5),
     ('VSYNC_O/S', -0.38, -0.5),
     ('D9_O/S', -0.38, -0.5),
     ('D8_O/S', -0.38, -0.5),
     ('D7_O/S', -0.38, -0.5),
     ('D6_O/S', -0.38, -0.5),
     ('D5_O/S', -0.38, -0.5),
     ('D4_O/S', -0.38, -0.5),
     ('D3_O/S', -0.38, -0.5),
     ('D2_O/S', -0.38, -0.5),
     ('D1_O/S', -0.38, -0.5),
     ('D0_O/S', -0.38, -0.5),
     ('SCL_O/S', -0.38, -0.5),
     ('SDA_O/S', -0.38, -0.5),
     ('RSTB_O/S', -0.38, -0.5),
     ('PWDN_O/S', -0.38, -0.5),
     ('DVDD_O/S', -0.32, -0.34),
     ('VRamp_O/S', -0.4, -0.5),
     ('VH_O/S', -0.4, -0.5),
     ('VN1_O/S', 0.5, 0.4),
     ('EXCLK_O/S', -0.4, -0.5),
     ('PCLK_Leakage/iiL', 0.005, -0.02),
     ('HSYNC_Leakage/iiL', 0.005, -0.02),
     ('VSYNC_Leakage/iiL', 0.005, -0.02),
     ('D9_Leakage/iiL', 0.005, -0.02),
     ('D8_Leakage/iiL', 0.005, -0.02),
     ('D7_Leakage/iiL', 0.005, -0.02),
     ('D6_Leakage/iiL', 0.005, -0.02),
     ('D5_Leakage/iiL', 0.005, -0.02),
     ('D4_Leakage/iiL', 0.005, -0.02),
     ('D3_Leakage/iiL', 0.005, -0.02),
     ('D2_Leakage/iiL', 0.005, -0.02),
     ('D1_Leakage/iiL', 0.02, -0.02),
     ('D0_Leakage/iiL', 0.02, -0.02),
     ('SCL_Leakage/iiL', 0.02, -0.02),
     ('SDA_Leakage/iiL', 0.02, -0.02),
     ('RSTB_Leakage/iiL', -0.15, -0.35),
     ('PWDN_Leakage/iiL', 0.1, -0.1),
     ('EXCLK_Leakage/iiL', 0.02, -0.02),
     ('PCLK_Leakage/iiH', 0.02, -0.02),
     ('HSYNC_Leakage/iiH', 0.02, -0.02),
     ('VSYNC_Leakage/iiH', 0.02, -0.02),
     ('D9_Leakage/iiH', 0.005, -0.02),
     ('D8_Leakage/iiH', 0.005, -0.02),
     ('D7_Leakage/iiH', 0.005, -0.02),
     ('D6_Leakage/iiH', 0.005, -0.02),
     ('D5_Leakage/iiH', 0.005, -0.02),
     ('D4_Leakage/iiH', 0.005, -0.02),
     ('D3_Leakage/iiH', 0.005, -0.02),
     ('D2_Leakage/iiH', 0.005, -0.02),
     ('D1_Leakage/iiH', 32, 27),
     ('D0_Leakage/iiH', 32, 27),
     ('SCL_Leakage/iiH', 0.005, -0.02),
     ('SDA_Leakage/iiH', 0.005, -0.02),
     ('RSTB_Leakage/iiH', 0.06, -0.02),
     ('PWDN_Leakage/iiH', 1.5, 0.5),
     ('EXCLK_Leakage/iiH', 0.005, -0.02),
     ('iic_test', 1, 1),
     ('DVDD_voltage', 1.65, 1.45, 9),
     ('VH_voltage', 4.4, 4.1, 9),
     ('VN1_voltage', -1.3, -1.6, 9),
     ('Active_AVDD', 27, 23, 12),
     ('Active_DOVDD', 70, 50, 12),
     ('PWDN_AVDD', 10, 0, 8),
     ('PWDN_DOVDD', 50, 0, 8),
     ('PWDN_Total', 60, 10, 8),
     ('BLC_R', 100, 90),
     ('BLC_Gr', 100, 90),
     ('BLC_Gb', 100, 90),
     ('BLC_B', 100, 90),
     ('PLCK_Freq', 86.5, 86.3, 9),
     ('BK_DeadRowExBPix_R', 0, 0, 15),
     ('BK_DeadRowExBPix_Gr', 0, 0, 15),
     ('BK_DeadRowExBPix_Gb', 0, 0, 15),
     ('BK_DeadRowExBPix_B', 0, 0, 15),
     ('BK_DeadColExBPix_R', 0, 0, 14),
     ('BK_DeadColExBPix_Gr', 0, 0, 14),
     ('BK_DeadColExBPix_Gb', 0, 0, 14),
     ('BK_DeadColExBPix_B', 0, 0, 14),
     ('BK_Mean_R', 18, 14, 13),
     ('BK_Mean_Gr', 18, 14, 13),
     ('BK_Mean_Gb', 18, 14, 13),
     ('BK_Mean_B', 18, 14, 13),
     ('BK_StdDEV_R', 4, 2, 13),
     ('BK_StdDEV_Gr', 4, 2, 13),
     ('BK_StdDEV_Gb', 4, 2, 13),
     ('BK_StdDEV_B', 4, 2, 13),
     ('LT_DRow_R', 0, 0, 25),
     ('LT_DRow_Gr', 0, 0, 25),
     ('LT_DRow_Gb', 0, 0, 25),
     ('LT_DRow_B', 0, 0, 25),
     ('LT_DCol_R', 0, 0, 24),
     ('LT_DCol_Gr', 0, 0, 24),
     ('LT_DCol_Gb', 0, 0, 24),
     ('LT_DCol_B', 0, 0, 24),
     ('LT_DRow_Color', 0, 0, 25),
     ('LT_DCol_Color', 0, 0, 24),
     ('LT_Mean_R', 500, 400, 23),
     ('LT_Mean_Gr', 700, 600, 23),
     ('LT_Mean_Gb', 700, 600, 23),
     ('LT_Mean_B', 500, 420, 23),
     ('LT_StdDEV_R', 7, 4, 23),
     ('LT_StdDEV_Gr', 7, 4, 23),
     ('LT_StdDEV_Gb', 7, 4, 23),
     ('LT_StdDEV_B', 7, 4, 23),
     ('LT_RI_R', 95, 85, 23),
     ('LT_RI_Gr', 95, 85, 23),
     ('LT_RI_Gb', 95, 85, 23),
     ('LT_RI_B', 95, 85, 23),
     ('LT_Ratio_GrR', 1.6, 1.4, 23),
     ('LT_Ratio_GbR', 1.6, 1.4, 23),
     ('LT_Ratio_GrB', 1.6, 1.4, 23),
     ('LT_Ratio_GbB', 1.6, 1.4, 23),
     ('LT_Ratio_GbGr', 1.1, 1, 23),
     ('LT_LostBit', 0, 0, 23),
     ('LT_LostBitSNR_SumDIFF_R', 2, 0, 23),
     ('LT_LostBitSNR_SumDIFF_Gr', 2, 0, 23),
     ('LT_LostBitSNR_SumDIFF_Gb', 2, 0, 23),
     ('LT_LostBitSNR_SumDIFF_B', 2, 0, 23),
     ('LB_LT_Mean_R', 680, 580),
     ('LB_LT_Mean_Gr', 980, 840),
     ('LB_LT_Mean_Gb', 980, 840),
     ('LB_LT_Mean_B', 680, 580),
     ('LB_LT_LostBit', 1, 0, 23),
     ('LB_LT_LostBitSNR_SumDIFF_R', 3, 0, 23),
     ('LB_LT_LostBitSNR_SumDIFF_Gr', 3, 0, 23),
     ('LB_LT_LostBitSNR_SumDIFF_Gb', 3, 0, 23),
     ('LB_LT_LostBitSNR_SumDIFF_B', 3, 0, 23),
     ('FW_LT_DRow_R', 0, 0, 36),
     ('FW_LT_DRow_Gr', 0, 0, 36),
     ('FW_LT_DRow_Gb', 0, 0, 36),
     ('FW_LT_DRow_B', 0, 0, 36),
     ('FW_LT_DCol_R', 0, 0, 36),
     ('FW_LT_DCol_Gr', 0, 0, 36),
     ('FW_LT_DCol_Gb', 0, 0, 36),
     ('FW_LT_DCol_B', 0, 0, 36),
     ('FW_LT_DRow_Color', 0, 0, 36),
     ('FW_LT_DCol_Color', 0, 0, 36),
     ('FW_LT_Mean_R', 1023, 1023, 36),
     ('FW_LT_Mean_Gr', 1023, 1023, 36),
     ('FW_LT_Mean_Gb', 1023, 1023, 36),
     ('FW_LT_Mean_B', 1023, 1023, 36),
     ('FW_LT_StdDEV_R', 0, 0, 36),
     ('FW_LT_StdDEV_Gr', 0, 0, 36),
     ('FW_LT_StdDEV_Gb', 0, 0, 36),
     ('FW_LT_StdDEV_B', 0, 0, 36),
     ('FW_LT_RI_R', 100, 100),
     ('FW_LT_RI_Gr', 100, 100),
     ('FW_LT_RI_Gb', 100, 100),
     ('FW_LT_RI_B', 100, 100),
     ('FW_LT_Ratio_GrR', 1, 1),
     ('FW_LT_Ratio_GbR', 1, 1),
     ('FW_LT_Ratio_GrB', 1, 1),
     ('FW_LT_Ratio_GbB', 1, 1),
     ('FW_LT_Ratio_GbGr', 1, 1),
     ('LT_CornerLine', 0, 0, 26),
     ('LT_ScratchLine', 0, 0, 26),
     ('LT_Blemish', 0, 0, 31),
     ('LT_LineStripe', 0, 0, 27),
     ('LT_Particle', 0, 0, 32),
     ('BK_Cluster2', 0, 0, 30),
     ('LT_Cluster2', 0, 0, 30),
     ('BK_Cluster1', 0, 0, 29),
     ('LT_Cluster1', 0, 0, 29),
     ('WP_Count', 0, 0, 35),
     ('BK_Cluster3GrGb', 0, 0, 39),
     ('LT_Cluster3GrGb', 0, 0, 40),
     ('BK_Cluster3SubtractGrGb', 1, 0, 33),
     ('LT_Cluster3SubtractGrGb', 1, 0, 34),
     ('LB_BK_DeadRowExBPix_R', 0, 0, 45),
     ('LB_BK_DeadRowExBPix_Gr', 0, 0, 45),
     ('LB_BK_DeadRowExBPix_Gb', 0, 0, 45),
     ('LB_BK_DeadRowExBPix_B', 0, 0, 45),
     ('LB_BK_DeadColExBPix_R', 0, 0, 44),
     ('LB_BK_DeadColExBPix_Gr', 0, 0, 44),
     ('LB_BK_DeadColExBPix_Gb', 0, 0, 44),
     ('LB_BK_DeadColExBPix_B', 0, 0, 44),
     ('SR_LT_DRow_R', 0, 0, 55),
     ('SR_LT_DRow_Gr', 0, 0, 55),
     ('SR_LT_DRow_Gb', 0, 0, 55),
     ('SR_LT_DRow_B', 0, 0, 55),
     ('SR_LT_DCol_R', 0, 0, 54),
     ('SR_LT_DCol_Gr', 0, 0, 54),
     ('SR_LT_DCol_Gb', 0, 0, 54),
     ('SR_LT_DCol_B', 0, 0, 54),
     ('SR_LT_DRow_Color', 0, 0, 55),
     ('SR_LT_DCol_Color', 0, 0, 54),
     ('SR_LT_Mean_R', 480, 400, 53),
     ('SR_LT_Mean_Gr', 700, 600, 53),
     ('SR_LT_Mean_Gb', 700, 600, 53),
     ('SR_LT_Mean_B', 480, 400, 53),
     ('SR_LT_StdDEV_R', 8, 4, 53),
     ('SR_LT_StdDEV_Gr', 8, 4, 53),
     ('SR_LT_StdDEV_Gb', 8, 4, 53),
     ('SR_LT_StdDEV_B', 8, 4, 53),
     ('SR_LT_RI_R', 100, 90, 53),
     ('SR_LT_RI_Gr', 100, 90, 53),
     ('SR_LT_RI_Gb', 100, 90, 53),
     ('SR_LT_RI_B', 100, 90, 53),
     ('SR_LT_Ratio_GrR', 1.6, 1.4, 53),
     ('SR_LT_Ratio_GbR', 1.6, 1.4, 53),
     ('SR_LT_Ratio_GrB', 1.6, 1.4, 53),
     ('SR_LT_Ratio_GbB', 1.6, 1.4, 53),
     ('SR_LT_Ratio_GbGr', 1.1, 1, 53),
     ('SR_LT_LostBit', 1, 0, 53),
     ('SR_BK_DeadRowExBPix_R', 0, 0, 42),
     ('SR_BK_DeadRowExBPix_Gr', 0, 0, 42),
     ('SR_BK_DeadRowExBPix_Gb', 0, 0, 42),
     ('SR_BK_DeadRowExBPix_B', 0, 0, 42),
     ('SR_BK_DeadColExBPix_R', 0, 0, 41),
     ('SR_BK_DeadColExBPix_Gr', 0, 0, 41),
     ('SR_BK_DeadColExBPix_Gb', 0, 0, 41),
     ('SR_BK_DeadColExBPix_B', 0, 0, 41),
     ('SR_BK_Mean_R', 70, 60, 43),
     ('SR_BK_Mean_Gr', 70, 60, 43),
     ('SR_BK_Mean_Gb', 70, 60, 43),
     ('SR_BK_Mean_B', 70, 60, 43),
     ('SR_BK_StdDEV_R', 2, 0, 43),
     ('SR_BK_StdDEV_Gr', 2, 0, 43),
     ('SR_BK_StdDEV_Gb', 2, 0, 43),
     ('SR_BK_StdDEV_B', 2, 0, 43),
     # ('Diffuser2_LT_WeakLineRow_R', 0, 0, 72),
     # ('Diffuser2_LT_WeakLineRow_Gr', 0, 0, 72),
     # ('Diffuser2_LT_WeakLineRow_Gb', 0, 0, 72),
     # ('Diffuser2_LT_WeakLineRow_B', 0, 0, 72),
     # ('Diffuser2_LT_WeakLineCol_R', 0, 0, 71),
     # ('Diffuser2_LT_WeakLineCol_Gr', 0, 0, 71),
     # ('Diffuser2_LT_WeakLineCol_Gb', 0, 0, 71),
     # ('Diffuser2_LT_WeakLineCol_B', 0, 0, 71),
     ('BK_Z1_BT_DP_R', 4, 0),
     ('BK_Z1_BT_DP_Gr', 4, 0),
     ('BK_Z1_BT_DP_Gb', 4, 0),
     ('BK_Z1_BT_DP_B', 4, 0),
     ('BK_Z2_BT_DP_R', 4, 0),
     ('BK_Z2_BT_DP_Gr', 4, 0),
     ('BK_Z2_BT_DP_Gb', 4, 0),
     ('BK_Z2_BT_DP_B', 4, 0),
     ('BK_Z1_BT_WP_R', 4, 0),
     ('BK_Z1_BT_WP_Gr', 4, 0),
     ('BK_Z1_BT_WP_Gb', 4, 0),
     ('BK_Z1_BT_WP_B', 4, 0),
     ('BK_Z2_BT_WP_R', 4, 0),
     ('BK_Z2_BT_WP_Gr', 4, 0),
     ('BK_Z2_BT_WP_Gb', 4, 0),
     ('BK_Z2_BT_WP_B', 4, 0),
     ('LT_Z1_BT_DP_R', 0, 0),
     ('LT_Z1_BT_DP_Gr', 0, 0),
     ('LT_Z1_BT_DP_Gb', 0, 0),
     ('LT_Z1_BT_DP_B', 0, 0),
     ('LT_Z2_BT_DP_R', 0, 0),
     ('LT_Z2_BT_DP_Gr', 0, 0),
     ('LT_Z2_BT_DP_Gb', 0, 0),
     ('LT_Z2_BT_DP_B', 0, 0),
     ('LT_Z1_BT_WP_R', 0, 0),
     ('LT_Z1_BT_WP_Gr', 0, 0),
     ('LT_Z1_BT_WP_Gb', 0, 0),
     ('LT_Z1_BT_WP_B', 0, 0),
     ('LT_Z2_BT_WP_R', 0, 0),
     ('LT_Z2_BT_WP_Gr', 0, 0),
     ('LT_Z2_BT_WP_Gb', 0, 0),
     ('LT_Z2_BT_WP_B', 0, 0),
     ('LT_Z1_DK_WP_R', 0, 0),
     ('LT_Z1_DK_WP_Gr', 0, 0),
     ('LT_Z1_DK_WP_Gb', 0, 0),
     ('LT_Z1_DK_WP_B', 0, 0),
     ('LT_Z2_DK_WP_R', 0, 0),
     ('LT_Z2_DK_WP_Gr', 0, 0),
     ('LT_Z2_DK_WP_Gb', 0, 0),
     ('LT_Z2_DK_WP_B', 0, 0),
     ('LT_Z1_DK_DP_R', 0, 0),
     ('LT_Z1_DK_DP_Gr', 0, 0),
     ('LT_Z1_DK_DP_Gb', 0, 0),
     ('LT_Z1_DK_DP_B', 0, 0),
     ('LT_Z2_DK_DP_R', 0, 0),
     ('LT_Z2_DK_DP_Gr', 0, 0),
     ('LT_Z2_DK_DP_Gb', 0, 0),
     ('LT_Z2_DK_DP_B', 0, 0),
     ('BK_Z1_BT_DP', 9, 0),
     ('BK_Z2_BT_DP', 9, 0),
     ('BK_Z1_BT_WP', 9, 0),
     ('BK_Z2_BT_WP', 9, 0),
     ('LT_Z1_BT_DP', 0, 0),
     ('LT_Z2_BT_DP', 0, 0),
     ('LT_Z1_BT_WP', 0, 0),
     ('LT_Z2_BT_WP', 0, 0),
     ('LT_Z1_DK_DP', 0, 0),
     ('LT_Z2_DK_DP', 0, 0),
     ('LT_Z1_DK_WP', 0, 0),
     ('LT_Z2_DK_WP', 0, 0),
     ('Binning', 0, 0, 2)
     ],
    [('VSYNC_O/S', -0.4, -0.5),
     ('HSYNC_O/S', -0.4, -0.5),
     ('PCLK_O/S', -0.4, -0.5),
     ('EXCLK_O/S', -0.4, -0.5),
     ('RSTB_O/S', -0.4, -0.5),
     ('PWDN_O/S', -0.4, -0.5),
     ('SDA_O/S', -0.4, -0.5),
     ('SCL_O/S', -0.4, -0.5),
     ('D0_O/S', -0.4, -0.5),
     ('D1_O/S', -0.4, -0.5),
     ('D2_O/S', -0.4, -0.5),
     ('D3_O/S', -0.4, -0.5),
     ('D4_O/S', -0.4, -0.5),
     ('D5_O/S', -0.4, -0.5),
     ('D6_O/S', -0.4, -0.5),
     ('D7_O/S', -0.4, -0.5),
     ('D8_O/S', -0.4, -0.5),
     ('D9_O/S', -0.4, -0.5),
     ('MCP_O/S', -0.4, -0.5),
     ('MCN_O/S', -0.4, -0.5),
     ('MDP0_O/S', -0.4, -0.5),
     ('MDN0_O/S', -0.4, -0.5),
     ('MDP1_O/S', -0.4, -0.5),
     ('MDN1_O/S', -0.4, -0.5),
     ('AVDD_O/S', -0.4, -0.5),
     ('DOVDD_O/S', -0.4, -0.5),
     ('VRamp_O/S', -0.4, -0.5),
     ('VH_O/S', -0.4, -0.5),
     ('VN1_O/S', 0.4, 0.3),

     ('VSYNC_Leakage/iiL', 0.01, -0.1),
     ('HSYNC_Leakage/iiL', 0.01, -0.1),
     ('PCLK_Leakage/iiL', 0.01, -0.1),
     ('EXCLK_Leakage/iiL', 0.01, -0.1),
     ('RSTB_Leakage/iiL', 0.01, -0.2),
     ('PWDN_Leakage/iiL', 0.01, -0.1),
     ('SDA_Leakage/iiL', 0.01, -0.1),
     ('SCL_Leakage/iiL', 0.01, -0.1),
     ('D0_Leakage/iiL', 0.01, -0.1),
     ('D1_Leakage/iiL', 0.01, -0.1),
     ('D2_Leakage/iiL', 0.01, -0.1),
     ('D4_Leakage/iiL', 0.01, -0.1),
     ('D5_Leakage/iiL', 0.01, -0.1),
     ('D3_Leakage/iiL', 0.01, -0.1),
     ('D6_Leakage/iiL', 0.01, -0.1),
     ('D7_Leakage/iiL', 0.01, -0.1),
     ('D8_Leakage/iiL', 0.01, -0.1),
     ('D9_Leakage/iiL', 0.01, -0.1),
     ('MCP_Leakage/iiL', 0.01, -0.1),
     ('MCN_Leakage/iiL', 0.01, -0.1),
     ('MDP0_Leakage/iiL', 0.01, -0.1),
     ('MDN0_Leakage/iiL', 0.01, -0.1),
     ('MDP1_Leakage/iiL', 0.01, -0.1),
     ('MDN1_Leakage/iiL', 0.01, -0.1),

     ('VSYNC_Leakage/iiH', 0.05, -0.01),
     ('HSYNC_Leakage/iiH', 0.05, -0.01),
     ('PCLK_Leakage/iiH', 0.05, -0.01),
     ('EXCLK_Leakage/iiH', 0.05, -0.01),
     ('RSTB_Leakage/iiH', 0.05, -0.01),
     ('PWDN_Leakage/iiH', 0.5, 0.1),
     ('SDA_Leakage/iiH', 0.01, -0.01),
     ('SCL_Leakage/iiH', 0.01, -0.01),
     ('D0_Leakage/iiH', 20, 18),
     ('D1_Leakage/iiH', 20, 18),
     ('D2_Leakage/iiH', 0.05, -0.01),
     ('D4_Leakage/iiH', 0.05, -0.01),
     ('D5_Leakage/iiH', 0.05, -0.01),
     ('D3_Leakage/iiH', 0.05, -0.01),
     ('D6_Leakage/iiH', 0.05, -0.01),
     ('D7_Leakage/iiH', 0.05, -0.01),
     ('D8_Leakage/iiH', 0.05, -0.01),
     ('D9_Leakage/iiH', 0.05, -0.01),
     ('MCP_Leakage/iiH', 0.05, -0.01),
     ('MCN_Leakage/iiH', 0.05, -0.01),
     ('MDP0_Leakage/iiH', 0.05, -0.01),
     ('MDN0_Leakage/iiH', 0.05, -0.01),
     ('MDP1_Leakage/iiH', 0.05, -0.01),
     ('MDN1_Leakage/iiH', 0.05, -0.01),

     ('iic_test', 1, 1),
     ('DVDD_voltage', 1.65, 1.45, 9),
     ('VH_voltage', 3.3, 2.7, 9),
     ('VN1_voltage', -1.3, -1.45, 9),
     ('Active_AVDD', 43, 40, 12),
     ('Active_DOVDD', 51, 47, 12),
     ('PWDN_AVDD', 70, 35, 8),
     ('PWDN_DOVDD', 25, 15, 8),
     ('PWDN_Total', 100, 55, 8),

     ('BLC_R', 430, 330),
     ('BLC_Gr', 430, 330),
     ('BLC_Gb', 430, 330),
     ('BLC_B', 430, 330),
     ('PLCK_Freq', 86.5, 86.3, 93),

     ('BK_DeadRowExBPix_R', 0, 0, 15),
     ('BK_DeadRowExBPix_Gr', 0, 0, 15),
     ('BK_DeadRowExBPix_Gb', 0, 0, 15),
     ('BK_DeadRowExBPix_B', 0, 0, 15),
     ('BK_DeadColExBPix_R', 0, 0, 14),
     ('BK_DeadColExBPix_Gr', 0, 0, 14),
     ('BK_DeadColExBPix_Gb', 0, 0, 14),
     ('BK_DeadColExBPix_B', 0, 0, 14),

     ('BK_MixDCol_VfpnQty_R', 0, 0),
     ('BK_MixDCol_VfpnQty_Gr', 0, 0),
     ('BK_MixDCol_VfpnQty_Gb', 0, 0),
     ('BK_MixDCol_VfpnQty_B', 0, 0),

     ('BK_MixDCol_VFPN_MaxValue0_R', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue0_Gr', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue0_Gb', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue0_B', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue1_R', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue1_Gr', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue1_Gb', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue1_B', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue2_R', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue2_Gr', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue2_Gb', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue2_B', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue3_R', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue3_Gr', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue3_Gb', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue3_B', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue4_R', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue4_Gr', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue4_Gb', 1, -1),
     ('BK_MixDCol_VFPN_MaxValue4_B', 1, -1),
     ('BK_Mean_R', 18, 13, 13),
     ('BK_Mean_Gr', 18, 13, 13),
     ('BK_Mean_Gb', 18, 13, 13),
     ('BK_Mean_B', 18, 13, 13),
     ('BK_StdDEV_R', 1.4, 1.1, 13),
     ('BK_StdDEV_Gr', 1.4, 1.1, 13),
     ('BK_StdDEV_Gb', 1.4, 1.1, 13),
     ('BK_StdDEV_B', 1.4, 1.1, 13),

     ('LT_DRow_R', 0, 0, 25),
     ('LT_DRow_Gr', 0, 0, 25),
     ('LT_DRow_Gb', 0, 0, 25),
     ('LT_DRow_B', 0, 0, 25),
     ('LT_DCol_R', 0, 0, 24),
     ('LT_DCol_Gr', 0, 0, 24),
     ('LT_DCol_Gb', 0, 0, 24),
     ('LT_DCol_B', 0, 0, 24),
     ('LT_DRow_Color', 0, 0, 24),
     ('LT_DCol_Color', 0, 0, 24),
     ('LT_WeakLineRow_R', 0, 0, 25),
     ('LT_WeakLineRow_Gr', 0, 0, 25),
     ('LT_WeakLineRow_Gb', 0, 0, 25),
     ('LT_WeakLineRow_B', 0, 0, 25),
     ('LT_WeakLineCol_R', 0, 0, 24),
     ('LT_WeakLineCol_Gr', 0, 0, 24),
     ('LT_WeakLineCol_Gb', 0, 0, 24),
     ('LT_WeakLineCol_B', 0, 0, 24),
     ('LT_Mean_R', 420, 380, 23),
     ('LT_Mean_Gr', 700, 640, 23),
     ('LT_Mean_Gb', 700, 640, 23),
     ('LT_Mean_B', 460, 410, 23),
     ('LT_StdDEV_R', 7, 4, 23),
     ('LT_StdDEV_Gr', 10, 6, 23),
     ('LT_StdDEV_Gb', 10, 6, 23),
     ('LT_StdDEV_B', 7, 4, 23),
     ('LT_RI_R', 72, 63, 23),
     ('LT_RI_Gr', 68, 60, 23),
     ('LT_RI_Gb', 68, 60, 23),
     ('LT_RI_B', 68, 59, 23),
     ('LT_Ratio_GrR', 1.72, 1.6, 23),
     ('LT_Ratio_GbR', 1.72, 1.6, 23),
     ('LT_Ratio_GrB', 1.62, 1.5, 23),
     ('LT_Ratio_GbB', 1.62, 1.5, 23),
     ('LT_Ratio_GbGr', 1, 0.99, 23),
     ('LT_LostBit', 0, 0, 23),
     ('LT_LostBitSNR_SumDIFF_R', 2, 0, 23),
     ('LT_LostBitSNR_SumDIFF_Gr', 2, 0, 23),
     ('LT_LostBitSNR_SumDIFF_Gb', 2, 0, 23),
     ('LT_LostBitSNR_SumDIFF_B', 2, 0, 23),

     ('LBIT_LT_Mean_R', 580, 530),
     ('LBIT_LT_Mean_Gr', 970, 890),
     ('LBIT_LT_Mean_Gb', 970, 890),
     ('LBIT_LT_Mean_B', 640, 560),
     ('LBIT_LT_LostBit', 0, 0, 23),
     ('LBIT_LT_LostBitSNR_SumDIFF_R', 4, 1, 23),
     ('LBIT_LT_LostBitSNR_SumDIFF_Gr', 4, 1, 23),
     ('LBIT_LT_LostBitSNR_SumDIFF_Gb', 3, 1, 23),
     ('LBIT_LT_LostBitSNR_SumDIFF_B', 3, 1, 23),

     ('FW_LT_DRow_R', 0, 0, 36),
     ('FW_LT_DRow_Gr', 0, 0, 36),
     ('FW_LT_DRow_Gb', 0, 0, 36),
     ('FW_LT_DRow_B', 0, 0, 36),
     ('FW_LT_DCol_R', 0, 0, 36),
     ('FW_LT_DCol_Gr', 0, 0, 36),
     ('FW_LT_DCol_Gb', 0, 0, 36),
     ('FW_LT_DCol_B', 0, 0, 36),
     ('FW_LT_DRow_Color', 0, 0, 36),
     ('FW_LT_DCol_Color', 0, 0, 36),
     ('FW_LT_Mean_R', 1023, 1023, 36),
     ('FW_LT_Mean_Gr', 1023, 1023, 36),
     ('FW_LT_Mean_Gb', 1023, 1023, 36),
     ('FW_LT_Mean_B', 1023, 1023, 36),
     ('FW_LT_StdDEV_R', 0, 0, 36),
     ('FW_LT_StdDEV_Gr', 0, 0, 36),
     ('FW_LT_StdDEV_Gb', 0, 0, 36),
     ('FW_LT_StdDEV_B', 0, 0, 36),
     ('FW_LT_RI_R', 100, 90),
     ('FW_LT_RI_Gr', 100, 90),
     ('FW_LT_RI_Gb', 100, 90),
     ('FW_LT_RI_B', 100, 90),
     ('FW_LT_Ratio_GrR', 1, 1),
     ('FW_LT_Ratio_GbR', 1, 1),
     ('FW_LT_Ratio_GrB', 1, 1),
     ('FW_LT_Ratio_GbB', 1, 1),
     ('FW_LT_Ratio_GbGr', 1, 1),
     ('FW_LT_LostBit', 1, 1),

     ('BSun_BK_DeadRowExBPix_R', 0, 0, 48),
     ('BSun_BK_DeadRowExBPix_Gr', 0, 0, 48),
     ('BSun_BK_DeadRowExBPix_Gb', 0, 0, 48),
     ('BSun_BK_DeadRowExBPix_B', 0, 0, 48),
     ('BSun_BK_DeadColExBPix_R', 0, 0, 47),
     ('BSun_BK_DeadColExBPix_Gr', 0, 0, 47),
     ('BSun_BK_DeadColExBPix_Gb', 0, 0, 47),
     ('BSun_BK_DeadColExBPix_B', 0, 0, 47),
     ('BSun_BK_Mean_R', 69, 62),
     ('BSun_BK_Mean_Gr', 69, 62),
     ('BSun_BK_Mean_Gb', 69, 62),
     ('BSun_BK_Mean_B', 69, 62),
     ('BSun_BK_StdDEV_R', 1.9, 1.6),
     ('BSun_BK_StdDEV_Gr', 1.9, 1.6),
     ('BSun_BK_StdDEV_Gb', 1.9, 1.6),
     ('BSun_BK_StdDEV_B', 1.9, 1.6),

     ('LMFlip_LT_DRow_R', 0, 0, 58),
     ('LMFlip_LT_DRow_Gr', 0, 0, 58),
     ('LMFlip_LT_DRow_Gb', 0, 0, 58),
     ('LMFlip_LT_DRow_B', 0, 0, 58),
     ('LMFlip_LT_DCol_R', 0, 0, 57),
     ('LMFlip_LT_DCol_Gr', 0, 0, 57),
     ('LMFlip_LT_DCol_Gb', 0, 0, 57),
     ('LMFlip_LT_DCol_B', 0, 0, 57),
     ('LMFlip_LT_DRow_Color', 0, 0, 58),
     ('LMFlip_LT_DCol_Color', 0, 0, 57),
     ('LMFlip_LT_WeakLineRow_R', 0, 0, 58),
     ('LMFlip_LT_WeakLineRow_Gr', 0, 0, 58),
     ('LMFlip_LT_WeakLineRow_Gb', 0, 0, 58),
     ('LMFlip_LT_WeakLineRow_B', 0, 0, 58),
     ('LMFlip_LT_WeakLineCol_R', 0, 0, 57),
     ('LMFlip_LT_WeakLineCol_Gr', 0, 0, 57),
     ('LMFlip_LT_WeakLineCol_Gb', 0, 0, 57),
     ('LMFlip_LT_WeakLineCol_B', 0, 0, 57),
     ('LMFlip_LT_Mean_R', 420, 380, 56),
     ('LMFlip_LT_Mean_Gr', 700, 640, 56),
     ('LMFlip_LT_Mean_Gb', 700, 640, 56),
     ('LMFlip_LT_Mean_B', 460, 400, 56),
     ('LMFlip_LT_StdDEV_R', 6, 4, 56),
     ('LMFlip_LT_StdDEV_Gr', 10, 6, 56),
     ('LMFlip_LT_StdDEV_Gb', 10, 6, 56),
     ('LMFlip_LT_StdDEV_B', 7, 4, 56),
     ('LMFlip_LT_RI_R', 71, 64, 56),
     ('LMFlip_LT_RI_Gr', 68, 60, 56),
     ('LMFlip_LT_RI_Gb', 68, 60, 56),
     ('LMFlip_LT_RI_B', 66, 59, 56),
     ('LMFlip_LT_Ratio_GrR', 1.75, 1.6, 56),
     ('LMFlip_LT_Ratio_GbR', 1.75, 1.6, 56),
     ('LMFlip_LT_Ratio_GrB', 1.6, 1.5, 56),
     ('LMFlip_LT_Ratio_GbB', 1.6, 1.5, 56),
     ('LMFlip_LT_Ratio_GbGr', 1, 0.99, 56),
     ('LMFlip_LT_LostBit', 0, 0, 56),
     ('LMFlip_LT_LostBitSNR_SumDIFF_R', 2, 0, 56),
     ('LMFlip_LT_LostBitSNR_SumDIFF_Gr', 2, 0, 56),
     ('LMFlip_LT_LostBitSNR_SumDIFF_Gb', 2, 0, 56),
     ('LMFlip_LT_LostBitSNR_SumDIFF_B', 2, 0, 56),

     ('LT_CornerLine', 0, 0, 26),
     ('LT_ScratchLine', 0, 0, 26),
     ('LT_Blemish', 0, 0, 31),
     ('LT_LineStripe', 0, 0, 27),
     ('LT_Particle', 0, 0, 32),
     ('BK_Cluster2', 0, 0, 30),
     ('LT_Cluster2', 0, 0, 30),
     ('BK_Cluster1', 0, 0, 29),
     ('LT_Cluster1', 0, 0, 29),
     ('BK_Cluster3GrGb', 0, 0, 39),
     ('LT_Cluster3GrGb', 0, 0, 40),
     ('BK_Cluster3SubtractGrGb', 0, 0, 33),
     ('LT_Cluster3SubtractGrGb', 0, 0, 34),
     ('WP_Count', 0, 0, 35),

     ('BK32X_BK_BadPixel_Area', 0, 0, 75),
     ('BK32X_BK_MixDCol_DashQty_R', 0, 0, 51),
     ('BK32X_BK_MixDCol_DashQty_Gr', 0, 0, 51),
     ('BK32X_BK_MixDCol_DashQty_Gb', 0, 0, 51),
     ('BK32X_BK_MixDCol_DashQty_B', 0, 0, 51),
     ('BK32X_SP_BK_MixDCol_DashQty_R', 0, 0, 54),
     ('BK32X_SP_BK_MixDCol_DashQty_Gr', 0, 0, 54),
     ('BK32X_SP_BK_MixDCol_DashQty_Gb', 0, 0, 54),
     ('BK32X_SP_BK_MixDCol_DashQty_B', 0, 0, 54),
     ('BK32X_BK_MixDCol_DASH_DeltaAvg_R', 15, 5),
     ('BK32X_BK_MixDCol_DASH_DeltaAvg_Gr', 15, 5),
     ('BK32X_BK_MixDCol_DASH_DeltaAvg_Gb', 15, 5),
     ('BK32X_BK_MixDCol_DASH_DeltaAvg_B', 15, 5),
     ('BK32X_BK_MixDCol_DASH_MaxValue0_R', 20, 8),
     ('BK32X_BK_MixDCol_DASH_MaxValue0_Gr', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue0_Gb', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue0_B', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue1_R', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue1_Gr', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue1_Gb', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue1_B', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue2_R', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue2_Gr', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue2_Gb', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue2_B', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue3_R', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue3_Gr', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue3_Gb', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue3_B', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue4_R', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue4_Gr', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue4_Gb', 20, 7),
     ('BK32X_BK_MixDCol_DASH_MaxValue4_B', 20, 7),
     ('BK32X_BK_Mean_R', 30, 10),
     ('BK32X_BK_Mean_Gr', 30, 10),
     ('BK32X_BK_Mean_Gb', 30, 10),
     ('BK32X_BK_Mean_B', 30, 10),
     ('BK32X_BK_StdDEV_R', 4, 1),
     ('BK32X_BK_StdDEV_Gr', 4, 1),
     ('BK32X_BK_StdDEV_Gb', 4, 1),
     ('BK32X_BK_StdDEV_B', 4, 1),
     ('BK_Cluster3_2', 0, 0),
     ('LT_Cluster3_2', 0, 0),

     ('MIPI_One_W1_FixedPattern', 0, 0, 94),

     ('MIPI_LT_DRow_R', 0, 0, 65),
     ('MIPI_LT_DRow_Gr', 0, 0, 65),
     ('MIPI_LT_DRow_Gb', 0, 0, 65),
     ('MIPI_LT_DRow_B', 0, 0, 65),
     ('MIPI_LT_DCol_R', 0, 0, 64),
     ('MIPI_LT_DCol_Gr', 0, 0, 64),
     ('MIPI_LT_DCol_Gb', 0, 0, 64),
     ('MIPI_LT_DCol_B', 0, 0, 64),
     ('MIPI_LT_DRow_Color', 0, 0, 65),
     ('MIPI_LT_DCol_Color', 0, 0, 64),
     ('MIPI_LT_WeakLineRow_R', 0, 0),
     ('MIPI_LT_WeakLineRow_Gr', 0, 0),
     ('MIPI_LT_WeakLineRow_Gb', 0, 0),
     ('MIPI_LT_WeakLineRow_B', 0, 0),
     ('MIPI_LT_WeakLineCol_R', 0, 0),
     ('MIPI_LT_WeakLineCol_Gr', 0, 0),
     ('MIPI_LT_WeakLineCol_Gb', 0, 0),
     ('MIPI_LT_WeakLineCol_B', 0, 0),
     ('MIPI_LT_Mean_R', 420, 380, 63),
     ('MIPI_LT_Mean_Gr', 700, 640, 63),
     ('MIPI_LT_Mean_Gb', 700, 640, 63),
     ('MIPI_LT_Mean_B', 460, 400, 63),
     ('MIPI_LT_StdDEV_R', 7, 4, 63),
     ('MIPI_LT_StdDEV_Gr', 9, 6, 63),
     ('MIPI_LT_StdDEV_Gb', 9, 6, 63),
     ('MIPI_LT_StdDEV_B', 7, 4, 63),
     ('MIPI_LT_RI_R', 70, 60, 63),
     ('MIPI_LT_RI_Gr', 68, 59, 63),
     ('MIPI_LT_RI_Gb', 68, 59, 63),
     ('MIPI_LT_RI_B', 68, 59, 63),
     ('MIPI_LT_Ratio_GrR', 1.75, 1.6, 63),
     ('MIPI_LT_Ratio_GbR', 1.75, 1.6, 63),
     ('MIPI_LT_Ratio_GrB', 1.6, 1.5, 63),
     ('MIPI_LT_Ratio_GbB', 1.6, 1.5, 63),
     ('MIPI_LT_Ratio_GbGr', 1, 0.99, 63),
     ('MIPI_LT_LostBit', 0, 0, 63),
     ('MIPI_LT_LostBitSNR_SumDIFF_R', 3, 0, 63),
     ('MIPI_LT_LostBitSNR_SumDIFF_Gr', 3, 0, 63),
     ('MIPI_LT_LostBitSNR_SumDIFF_Gb', 3, 0, 63),
     ('MIPI_LT_LostBitSNR_SumDIFF_B', 3, 0, 63),

     ('MIPI_LBIT_LT_Mean_R', 580, 520),
     ('MIPI_LBIT_LT_Mean_Gr', 970, 890),
     ('MIPI_LBIT_LT_Mean_Gb', 960, 890),
     ('MIPI_LBIT_LT_Mean_B', 640, 560),
     ('MIPI_LBIT_LT_LostBit', 0, 0, 63),
     ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_R', 4, 1, 63),
     ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_Gr', 4, 1, 63),
     ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_Gb', 4, 1, 63),
     ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_B', 4, 1, 63),

     ('BK_Z1_BT_DP_R', 0, 0),
     ('BK_Z1_BT_DP_Gr', 0, 0),
     ('BK_Z1_BT_DP_Gb', 0, 0),
     ('BK_Z1_BT_DP_B', 0, 0),
     ('BK_Z2_BT_DP_R', 0, 0),
     ('BK_Z2_BT_DP_Gr', 0, 0),
     ('BK_Z2_BT_DP_Gb', 0, 0),
     ('BK_Z2_BT_DP_B', 0, 0),
     ('BK_Z1_BT_WP_R', 0, 0),
     ('BK_Z1_BT_WP_Gr', 0, 0),
     ('BK_Z1_BT_WP_Gb', 0, 0),
     ('BK_Z1_BT_WP_B', 0, 0),
     ('BK_Z2_BT_WP_R', 0, 0),
     ('BK_Z2_BT_WP_Gr', 0, 0),
     ('BK_Z2_BT_WP_Gb', 0, 0),
     ('BK_Z2_BT_WP_B', 0, 0),
     ('LT_Z1_BT_DP_R', 0, 0),
     ('LT_Z1_BT_DP_Gr', 0, 0),
     ('LT_Z1_BT_DP_Gb', 0, 0),
     ('LT_Z1_BT_DP_B', 0, 0),
     ('LT_Z2_BT_DP_R', 0, 0),
     ('LT_Z2_BT_DP_Gr', 0, 0),
     ('LT_Z2_BT_DP_Gb', 0, 0),
     ('LT_Z2_BT_DP_B', 0, 0),
     ('LT_Z1_BT_WP_R', 0, 0),
     ('LT_Z1_BT_WP_Gr', 0, 0),
     ('LT_Z1_BT_WP_Gb', 0, 0),
     ('LT_Z1_BT_WP_B', 0, 0),
     ('LT_Z2_BT_WP_R', 0, 0),
     ('LT_Z2_BT_WP_Gr', 0, 0),
     ('LT_Z2_BT_WP_Gb', 0, 0),
     ('LT_Z2_BT_WP_B', 0, 0),
     ('LT_Z1_DK_WP_R', 0, 0),
     ('LT_Z1_DK_WP_Gr', 0, 0),
     ('LT_Z1_DK_WP_Gb', 0, 0),
     ('LT_Z1_DK_WP_B', 0, 0),
     ('LT_Z2_DK_WP_R', 0, 0),
     ('LT_Z2_DK_WP_Gr', 0, 0),
     ('LT_Z2_DK_WP_Gb', 0, 0),
     ('LT_Z2_DK_WP_B', 0, 0),
     ('LT_Z1_DK_DP_R', 0, 0),
     ('LT_Z1_DK_DP_Gr', 0, 0),
     ('LT_Z1_DK_DP_Gb', 0, 0),
     ('LT_Z1_DK_DP_B', 0, 0),
     ('LT_Z2_DK_DP_R', 0, 0),
     ('LT_Z2_DK_DP_Gr', 0, 0),
     ('LT_Z2_DK_DP_Gb', 0, 0),
     ('LT_Z2_DK_DP_B', 0, 0),
     ('BK_Z1_BT_DP', 0, 0),
     ('BK_Z2_BT_DP', 0, 0),
     ('BK_Z1_BT_WP', 0, 0),
     ('BK_Z2_BT_WP', 0, 0),
     ('LT_Z1_BT_DP', 0, 0),
     ('LT_Z2_BT_DP', 0, 0),
     ('LT_Z1_BT_WP', 0, 0),
     ('LT_Z2_BT_WP', 0, 0),
     ('LT_Z1_DK_DP', 0, 0),
     ('LT_Z2_DK_DP', 0, 0),
     ('LT_Z1_DK_WP', 0, 0),
     ('LT_Z2_DK_WP', 0, 0),

     ('Binning', 0, 0, 2),
     ]
]

golden_data = [
    ['GoldenHigh', '', '', ''],
    ['GoldenLow', '', '', '']
]


def parse_file(file):
    """
    parse file
    get basic information,goldendata result,binningcheck result,nanchipno result and summary result
    """
    global high_limit_row_num
    data = []
    # get file data
    with open(file) as f:
        csv_reader = reader(f)
        for row in csv_reader:
            data.append(row)

    # get row and column of last test item
    if project_id == 0:
        search_last_test_item = search_string(data, 'Full_Error')
    elif project_id == 1:
        search_last_test_item = search_string(data, 'ChipVer')
    if not search_last_test_item:
        exit()
    else:
        test_item_row_num = search_last_test_item[0]
        last_test_item_col_num = search_last_test_item[1]
    high_limit_row_num = test_item_row_num + 2
    low_limit_row_num = test_item_row_num + 3

    # get row and column of last DC test item
    search_pwdn_total = search_string(data, 'PWDN_Total')
    if not search_pwdn_total:
        exit()
    else:
        pwdn_total_col_num = search_pwdn_total[1]

    # get row and column of Binning
    search_binning = search_string(data, 'Binning')
    if not search_binning:
        exit()
    else:
        binning_col_num = search_binning[1]

    # get column of iic_test
    search_iic_test = search_string(data, 'iic_test')
    if not search_iic_test:
        exit()
    else:
        iic_test_col_num = search_iic_test[1]

    # get row of first register
    first_register_row_num = len(data)
    for i in range(test_item_row_num + row_offset, len(data)):
        try:
            int(data[i][0])
        except:
            first_register_row_num = i
            break

    # fill '' to align with last test item col num
    for i in range(0, len(data)):
        add_count = last_test_item_col_num + 1 - len(data[i])
        if add_count > 0:
            for j in range(add_count):
                data[i].append('')

    # golden data----------------------------
    row_count = len(data)

    # get row number with null value
    exist_nan_row_list = []
    for i in range(test_item_row_num + row_offset, first_register_row_num):
        for j in range(last_test_item_col_num - 1):
            if len(data[i][j].strip()) == 0:
                exist_nan_row_list.append(i)
                break

    golden_data_result = []
    golden_data_file_widgets = ['ParseFile-GoldenData: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',
                                FileTransferSpeed()]
    golden_data_pbar = ProgressBar(widgets=golden_data_file_widgets, maxval=row_count).start()
    for row_num in range(row_count):
        row_data = []
        for col_num in range(last_test_item_col_num + 1):
            value = data[row_num][col_num]
            if col_offset <= col_num <= binning_col_num and high_limit_row_num <= row_num <= low_limit_row_num:
                # fill color of limit value is green
                row_data.append((value, '008000'))
            elif col_num == 0 and row_num in exist_nan_row_list:
                # fill color of first value of exist nan row is purple
                row_data.append((value, 'A020F0'))
            elif col_offset <= col_num <= binning_col_num and test_item_row_num + row_offset <= row_num < first_register_row_num:
                try:
                    value_convert = float(value)
                    high_limit_data = data[high_limit_row_num][col_num]
                    try:
                        high_limit = float(high_limit_data)
                    except:
                        high_limit = high_limit_data
                    low_limit_data = data[low_limit_row_num][col_num]
                    try:
                        low_limit = float(low_limit_data)
                    except:
                        low_limit = low_limit_data
                    if value_convert == int(value_convert):
                        value_convert = int(value_convert)
                    if golden_data[1][col_num] <= value_convert <= golden_data[0][col_num]:
                        # fill color of within the golden limit value is white
                        row_data.append((value_convert, 'FFFFFF'))
                    elif high_limit == 'N' or (high_limit != 'N' and (
                                        low_limit <= value_convert < golden_data[1][col_num] or golden_data[0][
                                col_num] < value_convert <= high_limit)):
                        # fill color of following scenario value is yellow
                        # 1.over golden limit and limit is N
                        # 2.over golden limit and wihtin limit
                        row_data.append((value_convert, 'FFFF00'))
                    else:
                        # fill color of over limit is red
                        row_data.append((value_convert, 'FF0000'))
                except:
                    if not value.strip():
                        # fill color of '' is purple
                        row_data.append((value, 'A020F0'))
                    elif col_num == iic_test_col_num and value != '1':
                        # fill color of iic_test not 1 is yellow
                        row_data.append((value, 'FFFF00'))
            else:
                # set '' when value is nan
                if isinstance(value, float) and isnan(value):
                    value = ''
                # fill color is white
                row_data.append((value, 'FFFFFF'))
        golden_data_result.append(row_data)
        if row_num % 1000 == 0 or row_num == row_count - 1:
            # update bar when row num divisible by 1000 or is last row count
            golden_data_pbar.update(row_num + 1)
    golden_data_pbar.finish()

    # binning check----------------------------
    bin_definition = bin_definition_list[project_id]
    binning_check_result = []
    binning_check_widgets = ['ParseFile-BinningCheck: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',
                             FileTransferSpeed()]
    binning_check_pbar = ProgressBar(widgets=binning_check_widgets, maxval=first_register_row_num).start()
    for row_num in range(test_item_row_num + row_offset, first_register_row_num):
        # set row_softbin_index is last index
        row_softbin_index = len(bin_definition) - 1
        for col_num in range(col_offset, binning_col_num + 1):
            test_item_name = data[test_item_row_num][col_num].strip()
            if test_item_name == 'AVDD_O/S':
                # JX828 skip AVDD_O/S
                continue
            else:
                high_limit_data = data[high_limit_row_num][col_num]
                low_limit_data = data[low_limit_row_num][col_num]
            try:
                high_limit = float(high_limit_data)
                low_limit = float(low_limit_data)
                try:
                    value = data[row_num][col_num]
                    value_convert = float(value)
                    if value_convert == int(value_convert):
                        value_convert = int(value_convert)
                    if value_convert < low_limit or high_limit < value_convert:
                        # over limit
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == test_item_name:
                                if row_softbin_index > i:
                                    # set row_softbin_index is test_item_name's index when test_item_name's index less than row_softbin_index
                                    row_softbin_index = i
                except:
                    # value is ''
                    for i in range(len(bin_definition)):
                        if bin_definition[i][0] == test_item_name:
                            if row_softbin_index > i - 1:
                                # set row_softbin_index is test_item_name's index-1 when test_item_name's index less than row_softbin_index
                                row_softbin_index = i - 1
            except:
                # limit is N or nan
                try:
                    value = data[row_num][col_num]
                    float(value)
                    if test_item_name == 'iic_test' and value == '0':
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == 'iic_test':
                                if row_softbin_index > i:
                                    # set row_softbin_index is test_item_name's index when test_item_name's index less than row_softbin_index
                                    row_softbin_index = i
                except:
                    # value is ''
                    for i in range(len(bin_definition)):
                        if bin_definition[i][0] == test_item_name:
                            if row_softbin_index > i:
                                # set row_softbin_index is test_item_name's index-1 when test_item_name's index less than row_softbin_index
                                row_softbin_index = i - 1

        if bin_definition[row_softbin_index][1] != int(data[row_num][2]):
            # caculated value is not equal to SW_BIN value
            binning_check_result.append(
                "              SB_BIN error of chipNo " + data[row_num][
                    0] + " : according to the priority,swbin should be " + str(
                    bin_definition[row_softbin_index][1]) + " ,but in CSV it's " + data[row_num][2] + "\n")
        if bin_definition[row_softbin_index][2] != int(data[row_num][3]):
            # caculated value is not equal to hW_BIN value
            binning_check_result.append(
                "              hW_BIN error of chipNo " + data[row_num][
                    0] + " : according to the priority,hwbin should be " + str(
                    bin_definition[row_softbin_index][2]) + " ,but in CSV it's " + data[row_num][3] + "\n")
        if row_num % 1000 == 0 or row_num == first_register_row_num - 1:
            # update bar when row num divisible by 1000 or is last chipno row
            binning_check_pbar.update(row_num + 1)
    binning_check_pbar.finish()

    # nan chipno----------------------------
    dc_nan_chipno = []
    image_nan_chipno = []
    for i in range(test_item_row_num + row_offset, first_register_row_num):
        for j in range(col_offset, pwdn_total_col_num + 1):
            if len(data[i][j].strip()) == 0:
                # append value which is '' in columns col_offset to pwdn_total_col_num
                dc_nan_chipno.append(data[i][0])
                break
    for i in range(test_item_row_num + row_offset, first_register_row_num):
        for j in range(pwdn_total_col_num + 1, binning_col_num + 1):
            if len(data[i][j].strip()) == 0:
                # append value which is '' in columns pwdn_total_col_num+1 to binning_col_num
                image_nan_chipno.append(data[i][0])
                break
    nan_chipno_result = [dc_nan_chipno, image_nan_chipno]

    # summary----------------------------
    summary_result = []
    for group_by_id in range(1, 4):
        # 1:Site    2:SW_BIN    3:hW_BIN
        group_list = []
        for i in range(test_item_row_num + row_offset, first_register_row_num):
            # get value
            group_list.append(int(data[i][group_by_id]))
        # remove duplicate value
        format_group_list = list(set(group_list))
        # sort list
        format_group_list.sort()

        group_index = []
        for i in format_group_list:
            temp = [i]
            # find i in group_list
            data_list = find_item(group_list, i)
            if group_by_id == 1:
                temp_list = []
                for j in data_list:
                    # get the corresponding SW_BIN of Site
                    temp_list.append(data[test_item_row_num + row_offset + j][2])
                # remove duplicate value
                format_temp_list = list(set(temp_list))
                temp_index = []
                for m in format_temp_list:
                    temp_swbin = [m]
                    # find m in temp_list
                    temp_data_list = find_item(temp_list, m)
                    temp_swbin.append(temp_data_list)
                    temp_index.append(temp_swbin)
                temp.append(temp_index)
            else:
                temp.append(data_list)
            testitem_fail_count = []
            for col_num in range(col_offset, last_test_item_col_num + 1):
                test_item_name = data[test_item_row_num][col_num].strip()
                if test_item_name == 'AVDD_O/S':
                    # set AVDD_O/S's limit in JX828 project
                    high_limit_data = -0.2
                    low_limit_data = -0.6
                else:
                    high_limit_data = data[high_limit_row_num][col_num]
                    low_limit_data = data[low_limit_row_num][col_num]
                temp_list = [data[test_item_row_num][col_num], 0]
                try:
                    high_limit = float(high_limit_data)
                    low_limit = float(low_limit_data)
                    for j in data_list:
                        try:
                            value = data[test_item_row_num + row_offset + j][col_num]
                            value_convert = float(value)
                            if value_convert == int(value_convert):
                                value_convert = int(value_convert)
                            if value_convert < low_limit or high_limit < value_convert:
                                # count+1 when value over limit
                                temp_list[1] += 1
                        except:
                            # count+1 when value is ''
                            temp_list[1] += 1
                except:
                    # limit is N or nan
                    continue
                testitem_fail_count.append(temp_list)
            temp.append(testitem_fail_count)
            group_index.append(temp)
        summary_result.append(group_index)
    # parse file name
    file_name = basename(file).split('.')[0]
    # calculate chip count
    chip_count = first_register_row_num - test_item_row_num - row_offset
    # get lotno
    lotno = data[5][1]
    return file_name, chip_count, lotno, golden_data_result, binning_check_result, nan_chipno_result, summary_result


def save_data(analysis_folder, parse_data):
    """
    save data
    save golden data,binning check,nan chipno and summary to files
    """
    site_data = []
    softbin_data = []
    hardbin_data = []
    for data in parse_data:
        file_name = data[0]
        golden_parse_data = data[3]
        binning_check_parse_data = data[4]
        nan_chipno_parse_data = data[5]
        site_data.append(data[6][0])
        # sort softbin
        sort_data(data[6][1])
        softbin_data.append(data[6][1])
        hardbin_data.append(data[6][2])

        # golden data----------------------------
        golden_data_file = join(analysis_folder, file_name + ' vs GoldenData_' + now_time + '.xlsx')
        print(golden_data_file)
        golden_data_wb = Workbook()  # create file object
        golden_data_sheet = golden_data_wb.active  # get first sheet
        golden_data_sheet.freeze_panes = 'E19'  # set freeze panes

        irow = 1
        gather_data_widgets = ['GatherData-GoldenData: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',
                               FileTransferSpeed()]
        gather_data_pbar = ProgressBar(widgets=gather_data_widgets, maxval=len(golden_parse_data)).start()
        for i in range(len(golden_parse_data)):
            if i == high_limit_row_num:
                for m in range(len(golden_data[0])):
                    golden_data_sheet.cell(row=irow, column=m + 1).value = golden_data[0][m]
                    golden_data_sheet.cell(row=irow, column=m + 1).fill = PatternFill(fill_type='solid',
                                                                                      fgColor=golden_data_color)
                    golden_data_sheet.cell(row=irow, column=m + 1).border = border
                    if m == len(golden_data[0]) - 1:
                        for x in range(m + 1, len(golden_parse_data[0])):
                            golden_data_sheet.cell(row=irow, column=x + 1).border = border
                irow += 1
                for n in range(len(golden_data[1])):
                    golden_data_sheet.cell(row=irow, column=n + 1).value = golden_data[1][n]
                    golden_data_sheet.cell(row=irow, column=n + 1).fill = PatternFill(fill_type='solid',
                                                                                      fgColor=golden_data_color)
                    golden_data_sheet.cell(row=irow, column=n + 1).border = border
                    if n == len(golden_data[0]) - 1:
                        for x in range(n + 1, len(golden_parse_data[0])):
                            golden_data_sheet.cell(row=irow, column=x + 1).border = border
                irow += 1
            for j in range(len(golden_parse_data[i])):
                golden_data_sheet.cell(row=irow, column=j + 1).value = golden_parse_data[i][j][0]
                golden_data_sheet.cell(row=irow, column=j + 1).fill = PatternFill(fill_type='solid',
                                                                                  fgColor=golden_parse_data[i][j][1])
                golden_data_sheet.cell(row=irow, column=j + 1).border = border
            if i % 100 == 0 or i == len(golden_parse_data) - 1:
                gather_data_pbar.update(i + 1)
            irow += 1
        gather_data_pbar.finish()
        print("save golden data begin>>>>>>")
        golden_data_wb.save(golden_data_file)
        print("save golden data finished<<<<<<")

        # binning check----------------------------
        binning_check_file = join(analysis_folder, 'BinningCheck_Analysis' + now_time + '.txt')
        print("save binning check data begin>>>>>>")
        with open(binning_check_file, 'a') as f:
            f.write("            " + file_name + "：\n")
            if len(binning_check_parse_data) > 0:
                for item in binning_check_parse_data:
                    f.write(item)
            else:
                f.write('              No problem.\n')
        print("save binning check data finished<<<<<<")

        # nan chipno----------------------------
        nan_chipno_file = join(analysis_folder, 'NanChipno_Analysis' + now_time + '.txt')
        print("save nan chipno data begin>>>>>>")
        with open(nan_chipno_file, 'a') as f:
            f.write("            " + file_name + "：\n")
            if len(nan_chipno_parse_data[0]) > 0 or len(nan_chipno_parse_data[1]) > 0:
                if len(nan_chipno_parse_data[0]) == 0:
                    f.write("              (1) DC : no nan value.\n")
                else:
                    f.write(
                        "              (1) DC : " + str(len(nan_chipno_parse_data[0])) + " in total.They are : " + str(
                            nan_chipno_parse_data[0]) + "\n")
                if len(nan_chipno_parse_data[1]) == 0:
                    f.write("              (2) IMAGE : no nan value\n")
                else:
                    f.write("              (2) IMAGE : " + str(
                        len(nan_chipno_parse_data[1])) + " in total.They are : " + str(nan_chipno_parse_data[1]) + '\n')
            else:
                f.write("              No nan value.\n")
        print("save nan chipno data finished<<<<<<")

    lot_count = parse_data[0][1]
    lotno = parse_data[0][2]

    # Summary----------------------------
    summary_file = analysis_folder + '/Summary_Analysis_' + now_time + '.xlsx'
    summary_wb = Workbook()

    if project_id == 0:
        ok_hwbin_count = 2
    elif project_id == 1:
        ok_hwbin_count = 3

    begin_fail_swbin = 0
    for i in range(ok_hwbin_count):
        begin_fail_swbin += len(hwbin_to_swbin_list[project_id][i][1])

    color_list = ['99FFFF', '33FF00', 'FFFFCC', 'FFFF33', 'FF9900', 'FF0099', 'FF0000']
    swbin_list = []
    for i in range(len(hwbin_to_swbin_list[project_id])):
        for j in range(len(hwbin_to_swbin_list[project_id][i][1])):
            swbin_list.append([hwbin_to_swbin_list[project_id][i][1][j], color_list[i]])

    hardbin_sheet = summary_wb.create_sheet('HWBin')
    hardbin_sheet.freeze_panes = 'B2'
    summary_data = []
    for i in range(len(hardbin_data)):
        temp_list = []
        if i == 0:
            temp_list.append('FT')
        else:
            temp_list.append('RT' + str(i))
        test_count = 0
        for hw_bin in hwbin_to_swbin_list[project_id]:
            for j in range(len(hardbin_data[i])):
                if hw_bin[0] == hardbin_data[i][j][0]:
                    bin_count = len(hardbin_data[i][j][1])
                    break
                else:
                    bin_count = 0
            test_count += bin_count
            temp_list.append(bin_count)
        temp_list.append(test_count)
        pass_count = 0
        for m in range(ok_hwbin_count):
            pass_count += temp_list[1 + m]
        pass_percent = '{:.2%}'.format(pass_count / test_count)
        temp_list.append(pass_percent)
        summary_data.append(temp_list)
    irow = 1
    icol = 1
    hardbin_sheet.cell(row=irow, column=icol).value = lotno
    icol += 1
    for i in range(len(hwbin_to_swbin_list[project_id])):
        hardbin_sheet.cell(row=irow, column=icol).value = 'HWBin' + str(hwbin_to_swbin_list[project_id][i][0])
        icol += 1
    hardbin_sheet.cell(row=irow, column=icol).value = 'TestCount'
    icol += 1
    hardbin_sheet.cell(row=irow, column=icol).value = 'PassPercent'
    irow += 1
    for i in range(len(summary_data)):
        for j in range(len(summary_data[i])):
            hardbin_sheet.cell(row=irow, column=(j + 1)).value = summary_data[i][j]
            if j == 0:
                hardbin_sheet.cell(row=irow, column=(j + 1)).fill = PatternFill(fill_type='solid', fgColor=GREEN)
            elif 1 <= j < len(summary_data[i]) - 2:
                hardbin_sheet.cell(row=irow + 1, column=(j + 1)).value = '{:.2%}'.format(
                    summary_data[i][j] / summary_data[i][-2])
                hardbin_sheet.cell(row=irow + 1, column=(j + 1)).fill = PatternFill(fill_type='solid', fgColor=GREEN)
            elif j == len(summary_data[i]) - 2 and i > 0:
                compare_count = 0
                for m in range(ok_hwbin_count + 1, len(summary_data[i]) - 2):
                    compare_count += summary_data[i - 1][m]
                if summary_data[i][j] != compare_count:
                    # the number of test is not equal to the total number of chips failed in the previous test
                    if summary_data[i][j] > compare_count:
                        flag = '↓'
                    else:
                        flag = '↑'
                    hardbin_sheet.cell(row=irow, column=(j + 1)).fill = PatternFill(fill_type='solid', fgColor=RED)
                    hardbin_sheet.cell(row=irow + 1, column=(j + 1)).value = flag + str(compare_count)
                    hardbin_sheet.cell(row=irow + 1, column=(j + 1)).font = Font(color=RED, bold=True)
        irow += 2
    hardbin_sheet.cell(row=irow, column=1).value = 'Summary'
    hardbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=GREEN)
    # summary pass hwbin count : add all lots pass hwbin count
    pass_hwbin_count = [0] * ok_hwbin_count
    for i in range(len(summary_data)):
        for j in range(len(pass_hwbin_count)):
            pass_hwbin_count[j] += summary_data[i][j + 1]
    # summary total pass hwbin count : add all pass hwbin count
    total_pass_hwbin_count = 0
    for i in range(len(pass_hwbin_count)):
        hardbin_sheet.cell(row=irow, column=2 + i).value = pass_hwbin_count[i]
        total_pass_hwbin_count += pass_hwbin_count[i]
    # summary fail hwbin count : last lot's fail hwbin count
    for i in range(len(pass_hwbin_count) + 1, len(summary_data[-1]) - 2):
        hardbin_sheet.cell(row=irow, column=(i + 1)).value = summary_data[-1][i]
    hardbin_sheet.cell(row=irow, column=icol - 1).value = summary_data[0][-2]
    hardbin_sheet.cell(row=irow, column=icol).value = '{:.2%}'.format(total_pass_hwbin_count / summary_data[0][-2])

    for row in hardbin_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1:
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                cell.font = Font(bold=True)
                cell.alignment = alignment
            if cell.row == 2 and cell.column == hardbin_sheet.max_column:
                cell.fill = PatternFill(fill_type='solid', fgColor=GREEN)
            if cell.row == hardbin_sheet.max_row and cell.column == hardbin_sheet.max_column:
                cell.fill = PatternFill(fill_type='solid', fgColor=GREEN)

    hardsoftbin_sheet = summary_wb.create_sheet('HWBin-SWBin')
    hardsoftbin_sheet.freeze_panes = 'C2'
    irow = 1
    hardsoftbin_sheet.cell(row=irow, column=1).value = lotno
    hardsoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
    hardsoftbin_sheet.cell(row=irow, column=3).value = 'FT'
    hardsoftbin_sheet.cell(row=irow, column=3).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
    hardsoftbin_sheet.merge_cells(start_row=irow, end_row=irow, start_column=3, end_column=4)
    for i in range(1, len(softbin_data)):
        hardsoftbin_sheet.cell(row=irow, column=3 + 2 * i).value = 'RT' + str(i)
        hardsoftbin_sheet.cell(row=irow, column=3 + 2 * i).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
        hardsoftbin_sheet.merge_cells(start_row=irow, end_row=irow, start_column=3 + 2 * i, end_column=4 + 2 * i)
    irow += 1

    # sort swbin in hwbin from FT by swbin count from more to less
    swbin_sort_by_FT_list = []
    for i in range(len(hwbin_to_swbin_list[project_id])):
        temp_list = []
        for j in range(len(hwbin_to_swbin_list[project_id][i][1])):
            find_softbin = False
            for x in range(len(softbin_data[0])):
                if hwbin_to_swbin_list[project_id][i][1][j] == softbin_data[0][x][0]:
                    find_softbin = True
                    swbin_count = len(softbin_data[0][x][1])
                    temp_list.append((j, swbin_count))
            if not find_softbin:
                temp_list.append((j, 0))
        for m in range(len(temp_list) - 1):
            for n in range(m + 1, len(temp_list)):
                if temp_list[m][1] < temp_list[n][1]:
                    temp_list[m], temp_list[n] = temp_list[n], temp_list[m]
        temp_count_list = [hwbin_to_swbin_list[project_id][i][0]]
        for y in range(len(temp_list)):
            temp_count_list.append(hwbin_to_swbin_list[project_id][i][1][temp_list[y][0]])
        swbin_sort_by_FT_list.append(temp_count_list)

    summary_soft_count = []
    for i in range(len(swbin_sort_by_FT_list)):
        hardsoftbin_sheet.cell(row=irow, column=1).value = 'HWBin' + str(swbin_sort_by_FT_list[i][0])
        hardsoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=GREEN)
        hardsoftbin_sheet.cell(row=irow, column=1).font = Font(bold=True)
        for j in range(1, len(swbin_sort_by_FT_list[i])):
            hardsoftbin_sheet.cell(row=irow, column=2).value = 'SWBin' + str(swbin_sort_by_FT_list[i][j])
            temp_count = 0
            for m in range(len(softbin_data)):
                find_softbin = False
                for n in range(len(softbin_data[m])):
                    if swbin_sort_by_FT_list[i][j] == softbin_data[m][n][0]:
                        find_softbin = True
                        swbin_count = len(softbin_data[m][n][1])
                if not find_softbin:
                    swbin_count = 0
                if i in range(ok_hwbin_count):
                    # add the number of pass hwbin's swbin of all lots
                    temp_count += swbin_count
                elif m == len(softbin_data) - 1:
                    # set the number of fail hwbin's swbin of last lot
                    temp_count = swbin_count
                hardsoftbin_sheet.cell(row=irow, column=(2 * m + 3)).value = swbin_count
                hardsoftbin_sheet.cell(row=irow, column=(2 * m + 4)).value = '{:.2%}'.format(
                    swbin_count / summary_data[0][-2])
                hardsoftbin_sheet.cell(row=irow, column=(2 * m + 4)).fill = PatternFill(fill_type='solid',
                                                                                        fgColor=GREEN)
            irow += 1
            summary_soft_count.append(temp_count)
        summary_soft_count.append('')
        irow += 1

    irow = 1
    icol = 4 + 2 * len(softbin_data)
    hardsoftbin_sheet.cell(row=irow, column=icol).value = 'Summary'
    hardsoftbin_sheet.cell(row=irow, column=icol).fill = PatternFill(fill_type='solid', fgColor='FFA500')
    hardsoftbin_sheet.merge_cells(start_row=irow, end_row=irow, start_column=icol, end_column=icol + 1)
    irow += 1
    for i in range(len(summary_soft_count)):
        if isinstance(summary_soft_count[i], int):
            hardsoftbin_sheet.cell(row=irow, column=icol).value = summary_soft_count[i]
            hardsoftbin_sheet.cell(row=irow, column=icol + 1).value = '{:.2%}'.format(
                summary_soft_count[i] / summary_data[0][-2])
            hardsoftbin_sheet.cell(row=irow, column=icol + 1).fill = PatternFill(fill_type='solid', fgColor='FFA500')
        irow += 1

    for row in hardsoftbin_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1:
                cell.font = Font(bold=True)
                cell.alignment = alignment

    sitesoftbin_sheet = summary_wb.create_sheet('Site-SWBin')
    sitesoftbin_sheet.freeze_panes = 'B2'
    irow = 1
    sitesoftbin_sheet.cell(row=irow, column=1).value = lotno
    sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
    for i in range(len(site_data[0])):
        sitesoftbin_sheet.cell(row=irow, column=2 + i).value = 'Site' + str(site_data[0][i][0])
        sitesoftbin_sheet.cell(row=irow, column=2 + i).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
    sitesoftbin_sheet.merge_cells(start_row=irow, end_row=irow, start_column=3 + len(site_data[0]),
                                  end_column=4 + len(site_data[0]))
    sitesoftbin_sheet.cell(row=irow, column=3 + len(site_data[0])).value = 'Summary'
    sitesoftbin_sheet.cell(row=irow, column=3 + len(site_data[0])).fill = PatternFill(fill_type='solid',
                                                                                      fgColor='FFA500')
    irow += 1

    site_swbin_count = []
    for x in range(len(swbin_list)):
        temp_total_count = 0
        temp_list = []
        for i in range(len(site_data[0])):
            find_softbin = False
            for j in range(len(site_data[0][i][1])):
                if swbin_list[x][0] == int(site_data[0][i][1][j][0]):
                    temp_swbin_count = len(site_data[0][i][1][j][1])
                    find_softbin = True
            if not find_softbin:
                temp_swbin_count = 0
            temp_total_count += temp_swbin_count
            temp_list.append([temp_swbin_count, WHITE])
            if i == len(site_data[0]) - 1:
                temp_list.append([temp_total_count, 'FFA500'])
        site_swbin_count.append(temp_list)
    # add the number of fail swbin by all site
    # fill color of max value in fail swbin is green(all values are 0 do not fill green)
    # fill color of min value in fail swbin is red(multiple values of 0 do not fill red)
    site_fail_total_list = [0] * 16
    for i in range(begin_fail_swbin, len(site_swbin_count)):
        min_value = site_swbin_count[i][0][0]
        max_value = site_swbin_count[i][0][0]
        for m in range(1, len(site_swbin_count[i]) - 1):
            if min_value > site_swbin_count[i][m][0]:
                min_value = site_swbin_count[i][m][0]
            if max_value < site_swbin_count[i][m][0]:
                max_value = site_swbin_count[i][m][0]
        min_index = []
        max_index = []
        for j in range(len(site_swbin_count[i]) - 1):
            site_fail_total_list[j] += site_swbin_count[i][j][0]
            if site_swbin_count[i][j][0] == min_value:
                min_index.append(j)
            if site_swbin_count[i][j][0] == max_value:
                max_index.append(j)
        if min_value == 0 and len(min_index) == 1:
            site_swbin_count[i][min_index[0]][1] = GREEN
            for y in range(len(max_index)):
                site_swbin_count[i][max_index[y]][1] = RED
        elif min_value == 0 and max_value > 0:
            for y in range(len(max_index)):
                site_swbin_count[i][max_index[y]][1] = RED
        elif min_value > 0:
            for x in range(len(min_index)):
                site_swbin_count[i][min_index[x]][1] = GREEN
            for y in range(len(max_index)):
                site_swbin_count[i][max_index[y]][1] = RED

    for x in range(len(swbin_list)):
        sitesoftbin_sheet.cell(row=irow, column=1).value = 'SWBin' + str(swbin_list[x][0])
        sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=swbin_list[x][1])
        for y in range(len(site_swbin_count[x])):
            if y < len(site_swbin_count[x]) - 1:
                if site_swbin_count[x][y][0] > 0:
                    sitesoftbin_sheet.cell(row=irow, column=2 + y).value = '{:.4%}'.format(
                        site_swbin_count[x][y][0] / summary_data[0][-2])
                sitesoftbin_sheet.cell(row=irow, column=2 + y).fill = PatternFill(fill_type='solid',
                                                                                  fgColor=site_swbin_count[x][y][1])
            else:
                sitesoftbin_sheet.cell(row=irow, column=3 + y).value = site_swbin_count[x][y][0]
                sitesoftbin_sheet.cell(row=irow, column=4 + y).value = '{:.4%}'.format(
                    site_swbin_count[x][y][0] / summary_data[0][-2])
                sitesoftbin_sheet.cell(row=irow, column=4 + y).fill = PatternFill(fill_type='solid',
                                                                                  fgColor=site_swbin_count[x][y][1])
        irow += 1
    irow += 1
    sitesoftbin_sheet.merge_cells(start_row=irow, end_row=irow + 1, start_column=1, end_column=1)
    sitesoftbin_sheet.cell(row=irow, column=1).value = 'FailPercent'
    sitesoftbin_sheet.cell(row=irow, column=1).font = Font(bold=True)
    sitesoftbin_sheet.cell(row=irow, column=1).alignment = alignment
    sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor='FFA500')
    for i in range(len(site_fail_total_list)):
        sitesoftbin_sheet.cell(row=irow, column=2 + i).value = site_fail_total_list[i]
        sitesoftbin_sheet.cell(row=irow + 1, column=2 + i).value = '{:.4%}'.format(
            site_fail_total_list[i] / summary_data[0][-2])
        sitesoftbin_sheet.cell(row=irow + 1, column=2 + i).fill = PatternFill(fill_type='solid', fgColor='FFA500')

    for row in sitesoftbin_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1:
                cell.font = Font(bold=True)
                cell.alignment = alignment

    hwbin_testitem_sheet = summary_wb.create_sheet('HWBin-TestItem')
    hwbin_testitem_sheet.freeze_panes = 'B2'
    irow = 1
    hwbin_testitem_sheet.cell(row=irow, column=1).value = lot_count
    for i in range(len(hardbin_data[0][0][2])):
        hwbin_testitem_sheet.cell(row=irow, column=i + 2).value = hardbin_data[0][0][2][i][0]
    irow += 1
    for i in range(len(hardbin_data[0])):
        hwbin_testitem_sheet.cell(row=irow, column=1).value = 'HWBin' + str(hardbin_data[0][i][0])
        hwbin_testitem_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=GREEN)
        for j in range(len(hardbin_data[0][i][2])):
            hwbin_testitem_sheet.cell(row=irow, column=2 + j).value = hardbin_data[0][i][2][j][1]
            hwbin_testitem_sheet.cell(row=irow + 1, column=2 + j).value = '{:.2%}'.format(
                hardbin_data[0][i][2][j][1] / lot_count)
            if hardbin_data[0][i][2][j][1] > 0:
                # percent value greater than 0 are filled in red
                hwbin_testitem_sheet.cell(row=irow + 1, column=2 + j).fill = PatternFill(fill_type='solid',
                                                                                         fgColor=RED)
        irow += 2

    for row in hwbin_testitem_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1 and cell.column > 1:
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                cell.font = Font(bold=True)
                cell.alignment = alignment

    swbin_testitem_sheet = summary_wb.create_sheet('SWBin-TestItem')
    swbin_testitem_sheet.freeze_panes = 'B2'
    irow = 1
    swbin_testitem_sheet.cell(row=irow, column=1).value = lot_count
    for i in range(len(softbin_data[0][0][2])):
        swbin_testitem_sheet.cell(row=irow, column=i + 2).value = softbin_data[0][0][2][i][0]
    irow += 1
    for x in range(len(swbin_list)):
        swbin_testitem_sheet.cell(row=irow, column=1).value = 'SWBin' + str(swbin_list[x][0])
        swbin_testitem_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid',
                                                                         fgColor=swbin_list[x][1])
        for i in range(len(softbin_data[0])):
            if swbin_list[x][0] == softbin_data[0][i][0]:
                for j in range(len(softbin_data[0][i][2])):
                    swbin_testitem_sheet.cell(row=irow, column=2 + j).value = softbin_data[0][i][2][j][1]
                    swbin_testitem_sheet.cell(row=irow + 1, column=2 + j).value = '{:.2%}'.format(
                        softbin_data[0][i][2][j][1] / lot_count)
                    if softbin_data[0][i][2][j][1] > 0:
                        # percent value greater than 0 are filled in red
                        swbin_testitem_sheet.cell(row=irow + 1, column=2 + j).fill = PatternFill(fill_type='solid',
                                                                                                 fgColor=RED)
        irow += 2

    for row in swbin_testitem_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1 and cell.column > 1:
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                cell.font = Font(bold=True)
                cell.alignment = alignment

    site_testitem_sheet = summary_wb.create_sheet('Site-TestItem')
    site_testitem_sheet.freeze_panes = 'B2'
    irow = 1
    site_testitem_sheet.cell(row=irow, column=1).value = lot_count
    for i in range(len(site_data[0][0][2])):
        site_testitem_sheet.cell(row=irow, column=i + 2).value = site_data[0][0][2][i][0]
    irow += 1
    for i in range(len(site_data[0])):
        site_testitem_sheet.cell(row=irow, column=1).value = 'Site' + str(site_data[0][i][0])
        site_testitem_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid',
                                                                        fgColor=GREEN)
        for j in range(len(site_data[0][i][2])):
            site_testitem_sheet.cell(row=irow, column=2 + j).value = site_data[0][i][2][j][1]
            site_testitem_sheet.cell(row=irow + 1, column=2 + j).value = '{:.2%}'.format(
                site_data[0][i][2][j][1] / lot_count)
            if site_data[0][i][2][j][1] > 0:
                # percent value greater than 0 are filled in red
                site_testitem_sheet.cell(row=irow + 1, column=2 + j).fill = PatternFill(fill_type='solid',
                                                                                        fgColor=RED)
        irow += 2

    for row in site_testitem_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1 and cell.column > 1:
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                cell.font = Font(bold=True)
                cell.alignment = alignment

    for sheet_name in summary_wb.sheetnames:
        if sheet_name == 'Sheet':
            del summary_wb[sheet_name]
        else:
            set_column_width(summary_wb[sheet_name])
    print("save summary data begin>>>>>>")
    summary_wb.save(summary_file)
    print("save summary data finished<<<<<<")


def main():
    global project_id
    global golden_data

    # date folder path
    if argv.count('-d') == 0:
        print("Error：Date folder path is required.Format:-d D:\Date folder.")
        exit()
    else:
        date_folder = argv[argv.index('-d') + 1]
        for i in range(argv.index('-d') + 2, len(argv)):
            if not argv[i].startswith('-'):
                date_folder += (' ' + argv[i])
            else:
                break

    # project 0:F28,1:JX828
    if argv.count('-p') != 0:
        project_id = int(argv[argv.index('-p') + 1])

    # get project's golden data
    for i in range(len(golden_data_list[project_id])):
        golden_data[0].append(golden_data_list[project_id][i][1])
        golden_data[1].append(golden_data_list[project_id][i][2])

    lotno_names = listdir(date_folder)
    for name in lotno_names:
        folder = join(date_folder, name)
        if isdir(folder):
            # get CSV file under the folder
            file_list = get_filelist(folder, '.csv')
            if not file_list:
                exit()

            # analysis folder path
            if argv.count('-a') == 0:
                # default analysis folder
                analysis_folder = folder + '\Analysis'
            else:
                analysis_folder = argv[argv.index('-a') + 1]

            # create analysis folder
            mkdir(analysis_folder)

            parse_data = []
            for file in file_list:
                print(file)
                # parse file
                parse_data.append(parse_file(file))
            # save data
            save_data(analysis_folder, parse_data)


if __name__ == '__main__':
    main()
