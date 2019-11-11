# encoding:utf-8
# @Time     : 2019/10/24
# @Author   : Jerry Chou
# @File     :
# @Function : 1、多文件分析  2、校验SoftBin对应HardBin是否正确
import csv
import datetime
import os
from sys import argv

row_offset = 5
col_offset = 4

bin_definition = [('PCLK_O/S', 5, 5),
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
                  ('LT_CornerLine', 26, 4),
                  ('LT_ScratchLine', 26, 4),
                  ('LT_Blemish', 31, 4),
                  ('LT_LineStripe', 27, 4),
                  ('LT_Particle', 32, 4),
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
                  ('Diffuser2_LT_ImageCapture', 99, 5),
                  ('Diffuser2_LT_WeakLineRow_R', 72, 4),
                  ('Diffuser2_LT_WeakLineRow_Gr', 72, 4),
                  ('Diffuser2_LT_WeakLineRow_Gb', 72, 4),
                  ('Diffuser2_LT_WeakLineRow_B', 72, 4),
                  ('Diffuser2_LT_WeakLineCol_R', 71, 4),
                  ('Diffuser2_LT_WeakLineCol_Gr', 71, 4),
                  ('Diffuser2_LT_WeakLineCol_Gb', 71, 4),
                  ('Diffuser2_LT_WeakLineCol_B', 71, 4),
                  ('Binning', 2, 1),
                  ('All Pass', 1, 1)
                  ]


def parse_file(file, result_file):
    data = []
    with open(file) as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            data.append(row)

    for i in range(len(data)):
        try:
            binning_col_num = data[i].index('Binning')
            binning_row_num = i
            break
        except:
            pass
    col_count = binning_col_num + 1
    firstregister_row_num = len(data) - 1
    for i in range(binning_row_num + row_offset, len(data)):
        try:
            int(data[i][0])
        except:
            firstregister_row_num = i
            break

    file_name = os.path.basename(file)
    error_message = []
    for row_num in range(binning_row_num + row_offset, firstregister_row_num):
        row_softbin_index = len(bin_definition) - 1
        for col_num in range(col_offset, col_count):
            high_limit_data = data[binning_row_num + 2][col_num]
            low_limit_data = data[binning_row_num + 3][col_num]
            try:
                high_limit = float(high_limit_data)
                low_limit = float(low_limit_data)
                try:
                    value = data[row_num][col_num]
                    value_convert = float(value)
                    if value_convert == int(value_convert):
                        value_convert = int(value_convert)
                    if value_convert < low_limit or high_limit < value_convert:
                        test_item_name = data[binning_row_num][col_num].strip()
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == test_item_name:
                                if row_softbin_index > i:
                                    row_softbin_index = i
                except:
                    if data[binning_row_num][col_num].strip() == 'BK_DeadRowExBPix_R':
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == 'BK_DeadRowExBPix_R':
                                if row_softbin_index > i - 1:
                                    row_softbin_index = i - 1
                    elif data[binning_row_num][col_num].strip() == 'LT_DRow_R':
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == 'LT_DRow_R':
                                if row_softbin_index > i - 1:
                                    row_softbin_index = i - 1
                    elif data[binning_row_num][col_num].strip() == 'LB_LT_Mean_R':
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == 'LB_LT_Mean_R':
                                if row_softbin_index > i - 1:
                                    row_softbin_index = i - 1
                    elif data[binning_row_num][col_num].strip() == 'FW_LT_DRow_R':
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == 'FW_LT_DRow_R':
                                if row_softbin_index > i - 1:
                                    row_softbin_index = i - 1
                    elif data[binning_row_num][col_num].strip() == 'SR_LT_DRow_R':
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == 'SR_LT_DRow_R':
                                if row_softbin_index > i - 1:
                                    row_softbin_index = i - 1
                    elif data[binning_row_num][col_num].strip() == 'SR_BK_DeadRowExBPix_R':
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == 'SR_BK_DeadRowExBPix_R':
                                if row_softbin_index > i - 1:
                                    row_softbin_index = i - 1
                    elif data[binning_row_num][col_num].strip() == 'Diffuser2_LT_WeakLineRow_R':
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == 'Diffuser2_LT_WeakLineRow_R':
                                if row_softbin_index > i - 1:
                                    row_softbin_index = i - 1
            except:
                if data[binning_row_num][col_num] == 'iic_test' and data[row_num][col_num] == '0':
                    for i in range(len(bin_definition)):
                        if bin_definition[i][0] == 'iic_test':
                            if row_softbin_index > i:
                                row_softbin_index = i
        if bin_definition[row_softbin_index][1] != int(data[row_num][2]):
            error_message.append("ChipNo " + data[row_num][0] + " 的SB_BIN错误：根据优先级计算出来的swbin为 " + str(
                bin_definition[row_softbin_index][1]) + " ,CSV中为 " + data[row_num][2] + "\n")
        if bin_definition[row_softbin_index][2] != int(data[row_num][3]):
            error_message.append("ChipNo " + data[row_num][0] + " 的hW_BIN错误：根据优先级计算出来的hwbin为 " + str(
                bin_definition[row_softbin_index][2]) + " ,CSV中为 " + data[row_num][3] + "\n")
        print("解析文件：第 " + str(row_num + 1) + " 行")

    with open(result_file, 'a') as f:
        if len(error_message) > 0:
            f.write(file_name + " 分Bin可能存在问题的ChipNo：\n")
            for item in error_message:
                f.write(item)
        else:
            f.write(file_name + '：分Bin没有问题。\n')


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

    mkdir(analysis_folder)
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    result_file = os.path.join(analysis_folder, 'BinningCheck' + date + '.txt')

    for file in file_list:
        original_file = os.path.join(sourcefile_folder, file)
        # parse file
        parse_file(original_file, result_file)


if __name__ == '__main__':
    main()
