# encoding:utf-8
# @Time     : 2019/9/9 13:32
# @Author   : Jerry Chou
# @File     :
# @Function :
import csv
import os
import datetime, math
from sys import argv

from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side

row_offset = 5
col_offset = 4

golden_data_color = '00FFFF'  # 水绿色
iic_test = 'iic_test'


def get_golden_data():
    golden_data_list = [('PCLK_O/S', -0.38, -0.5),
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
                        ('Diffuser2_LT_WeakLineRow_R', 0, 0, 72),
                        ('Diffuser2_LT_WeakLineRow_Gr', 0, 0, 72),
                        ('Diffuser2_LT_WeakLineRow_Gb', 0, 0, 72),
                        ('Diffuser2_LT_WeakLineRow_B', 0, 0, 72),
                        ('Diffuser2_LT_WeakLineCol_R', 0, 0, 71),
                        ('Diffuser2_LT_WeakLineCol_Gr', 0, 0, 71),
                        ('Diffuser2_LT_WeakLineCol_Gb', 0, 0, 71),
                        ('Diffuser2_LT_WeakLineCol_B', 0, 0, 71),
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
                        ]
    golden_high_list = ['GoldenHigh', '', '', '']
    golden_low_list = ['GoldenLow', '', '', '']
    for i in range(len(golden_data_list)):
        golden_high_list.append(golden_data_list[i][1])
        golden_low_list.append(golden_data_list[i][2])
    return golden_high_list, golden_low_list


def parse_file(file, golden_data):
    data = []
    with open(file) as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            data.append(row)

    for i in range(len(data)):
        try:
            binning_col_num = data[i].index('Binning')
            break
        except:
            pass
    for i in range(0, len(data)):
        add_count = binning_col_num + 1 - len(data[i])
        if add_count > 0:
            for j in range(add_count):
                data[i].append('')

    for i in range(len(data)):
        try:
            data[i].index('ChipNo')
            chipno_row_num = i
            break
        except:
            pass
    col_count = binning_col_num + 1
    row_count = len(data)
    firstregister_row_num = len(data)
    for i in range(chipno_row_num + row_offset, len(data)):
        try:
            int(data[i][0])
        except:
            firstregister_row_num = i
            break
    exist_nan_row_list = []
    for i in range(chipno_row_num + row_offset, firstregister_row_num):
        for j in range(col_count):
            if len(data[i][j].strip()) == 0:
                exist_nan_row_list.append(i)
                break

    for i in range(len(data)):
        try:
            iic_test_col_num = data[i].index(iic_test)
            break
        except:
            pass

    result = []

    for row_num in range(row_count):
        row_data = []
        for col_num in range(col_count):
            value = data[row_num][col_num]
            if chipno_row_num + 2 <= row_num <= chipno_row_num + 3:
                row_data.append((value, '008000'))  # 纯绿
            elif col_num == 0 and row_num in exist_nan_row_list:
                row_data.append((value, 'A020F0'))  # purple
            elif col_num >= col_offset and chipno_row_num + row_offset <= row_num < firstregister_row_num:
                try:
                    value_convert = float(value)
                    high_limit_data = data[chipno_row_num + 2][col_num]
                    try:
                        high_limit = float(high_limit_data)
                    except:
                        high_limit = high_limit_data
                    low_limit_data = data[chipno_row_num + 3][col_num]
                    try:
                        low_limit = float(low_limit_data)
                    except:
                        low_limit = low_limit_data
                    if value_convert == int(value_convert):
                        value_convert = int(value_convert)
                    if golden_data[1][col_num] <= value_convert <= golden_data[0][col_num]:
                        row_data.append((value_convert, 'FFFFFF'))  # 白色
                    elif high_limit == 'N' or (high_limit != 'N' and (
                                        low_limit <= value_convert < golden_data[1][col_num] or golden_data[0][
                                col_num] < value_convert <= high_limit)):
                        row_data.append((value_convert, 'FFFF00'))  # 纯黄
                    else:
                        row_data.append((value_convert, 'FF0000'))  # 纯红
                except:
                    if value.isspace():
                        row_data.append((value, 'A020F0'))  # purple
                    elif col_num == iic_test_col_num and value != '1':
                        row_data.append((value, 'FFFF00'))  # 纯黄
            else:
                if isinstance(value, float) and math.isnan(value):
                    value = ''
                row_data.append((value, 'FFFFFF'))
        result.append(row_data)
        print("解析文件：第 " + str(row_num + 1) + " 行")
    return result


def analysis_data(file, data, golden_data):
    file_name = file.split('.')[0]
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    test_file_name = file_name + ' vs GoldenData_' + date + '.xlsx'

    wb = Workbook()  # 创建文件对象

    ws = wb.active  # 获取第一个sheet
    ws.freeze_panes = 'E19'

    border = Border(left=Side(border_style='thin', color='000000'),

                    right=Side(border_style='thin', color='000000'),

                    top=Side(border_style='thin', color='000000'),

                    bottom=Side(border_style='thin', color='000000'))
    irow = 1
    for i in range(len(data)):
        if i == 14:
            for m in range(len(golden_data[0])):
                ws.cell(row=irow, column=m + 1).value = golden_data[0][m]
                ws.cell(row=irow, column=m + 1).fill = PatternFill(fill_type='solid', fgColor=golden_data_color)
                ws.cell(row=irow, column=m + 1).border = border
            irow += 1
            for n in range(len(golden_data[1])):
                ws.cell(row=irow, column=n + 1).value = golden_data[1][n]
                ws.cell(row=irow, column=n + 1).fill = PatternFill(fill_type='solid', fgColor=golden_data_color)
                ws.cell(row=irow, column=n + 1).border = border
            irow += 1
        for j in range(len(data[i])):
            ws.cell(row=irow, column=j + 1).value = data[i][j][0]
            ws.cell(row=irow, column=j + 1).fill = PatternFill(fill_type='solid', fgColor=data[i][j][1])
            ws.cell(row=irow, column=j + 1).border = border
        print("组装Excel数据：第 " + str(i + 1) + " 行")
        irow += 1
    print("保存数据开始-----------------")
    wb.save(test_file_name)
    print("保存数据结束-----------------")


def mkdir(dir):
    dir = dir.strip()
    dir = dir.rstrip("\\")
    isExists = os.path.exists(dir)
    if not isExists:
        os.makedirs(dir)
        return True
    else:
        return False


def get_file(folder):
    result = []
    get_dir = os.listdir(folder)
    for dir in get_dir:
        sub_dir = os.path.join(folder, dir)
        if not os.path.isdir(sub_dir):
            result.append(dir)
    return result


def main():
    # Sourcefile folder path
    if argv.count('-s') == 0 and argv.count('-f') == 0:
        print(
            "Error：Sourcefile folder path 或 single file path为必填项，格式：“-s D:\sourcefile” 或 “-f D:\sourcefile\ST5-440mm-out1.csv”。")
        exit()

    if argv.count('-s') != 0:
        sourcefile_folder = argv[argv.index('-s') + 1]
        file_list = get_file(sourcefile_folder)

    if argv.count('-f') != 0:
        single_file = argv[argv.index('-f') + 1]
        sourcefile_folder = os.path.dirname(single_file)
        file_list = [os.path.basename(single_file)]

    # Analysis folder path
    if argv.count('-a') == 0:
        analysis_folder = sourcefile_folder + '\Analysis'
    else:
        analysis_folder = argv[argv.index('-a') + 1]

    # golden_data = parse_golden_data_file(golden_data_file)
    golden_data = get_golden_data()
    mkdir(analysis_folder)

    for file in file_list:
        original_file = os.path.join(sourcefile_folder, file)
        print(original_file)
        # parse file
        data = parse_file(original_file, golden_data)

        analysis_file = os.path.join(analysis_folder, file)
        print(analysis_file)
        # analysis data
        analysis_data(analysis_file, data, golden_data)


if __name__ == '__main__':
    main()
