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

last_os_testitem = 'EXCLK_O/S'
last_leakage_testitem = 'EXCLK_Leakage/iiH'
iic_test = 'iic_test'

SWBinToHWBin = [
    (5, 5),
    (6, 5),
    (7, 5),
    (9, 5),
    (12, 5),
    (8, 5),
    (15, 6),
    (14, 6),
    (13, 6),
    (25, 4),
    (24, 4),
    (23, 4),
    (36, 4),
    (26, 4),
    (31, 4),
    (27, 4),
    (32, 4),
    (30, 4),
    (29, 4),
    (35, 6),
    (39, 4),
    (40, 4),
    (33, 4),
    (34, 4),
    (45, 2),
    (44, 2),
    (55, 2),
    (54, 2),
    (53, 2),
    (42, 2),
    (41, 2),
    (43, 2),
    (70, 4),
    (72, 4),
    (71, 4),
    (2, 1),
    (1, 1)
]


def compare_swbin_priority(swbin1, swbin2):
    for i in range(len(SWBinToHWBin)):
        if SWBinToHWBin[i][0] == swbin1:
            swbin1_index = i
            break
    for i in range(len(SWBinToHWBin)):
        if SWBinToHWBin[i][0] == swbin2:
            swbin2_index = i
            break
    if swbin1_index <= swbin2_index:
        return swbin1
    else:
        return swbin2


def get_hardbin(swbin):
    for i in range(len(SWBinToHWBin)):
        if SWBinToHWBin[i][0] == swbin:
            return SWBinToHWBin[i][1]


def parse_file(file, result_file):
    data = []
    with open(file) as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            data.append(row)

    for i in range(len(data)):
        try:
            data[i].index('ChipNo')
            chipno_row_num = i
            break
        except:
            pass

    col_count = len(data[chipno_row_num])
    firstregister_row_num = len(data) - 1
    for i in range(chipno_row_num + row_offset, len(data)):
        try:
            int(data[i][0])
        except:
            firstregister_row_num = i
            break

    for i in range(len(data)):
        try:
            last_os_testitem_col_num = data[i].index(last_os_testitem)
            break
        except:
            pass

    for i in range(len(data)):
        try:
            last_leakage_testitem_col_num = data[i].index(last_leakage_testitem)
            break
        except:
            pass

    for i in range(len(data)):
        try:
            iic_test_col_num = data[i].index(iic_test)
            break
        except:
            pass

    with open(result_file, 'a') as f:
        f.write(file + " 分Bin可能存在问题的ChipNo：\n")
        for row_num in range(chipno_row_num + row_offset, firstregister_row_num):
            row_softbin_list = []
            for col_num in range(col_offset, col_count - 4):
                high_limit_data = data[chipno_row_num + 2][col_num]
                low_limit_data = data[chipno_row_num + 3][col_num]
                try:
                    high_limit = float(high_limit_data)
                    low_limit = float(low_limit_data)
                    try:
                        value = data[row_num][col_num]
                        value_convert = float(value)
                        if value_convert == int(value_convert):
                            value_convert = int(value_convert)
                        if value_convert < low_limit or high_limit < value_convert:
                            if col_num <= last_os_testitem_col_num:
                                row_softbin_list.append(5)
                            elif last_os_testitem_col_num < col_num <= last_leakage_testitem_col_num:
                                row_softbin_list.append(6)
                            elif data[chipno_row_num + 4][col_num] != 'N':
                                row_softbin_list.append(int(data[chipno_row_num + 4][col_num]))
                        else:
                            row_softbin_list.append(1)
                    except:
                        pass
                except:
                    if col_num == iic_test_col_num and data[row_num][col_num] != '1':
                        row_softbin_list.append(7)
            row_softbin = row_softbin_list[0]
            for softbin in row_softbin_list:
                row_softbin = compare_swbin_priority(row_softbin, softbin)
            if row_softbin != int(data[row_num][2]):
                f.write("ChipNo " + data[row_num][0] + " 的SB_BIN错误：根据优先级计算出来的swbin为 " + str(row_softbin) + " ,CSV中为 " +
                        data[row_num][2] + "\n")
            hardbin = get_hardbin(row_softbin)
            if hardbin != int(data[row_num][3]):
                f.write("ChipNo " + data[row_num][0] + " 的hW_BIN错误：根据优先级计算出来的hwbin为 " + str(hardbin) + " ,CSV中为 " +
                        data[row_num][3] + "\n")
            print("解析文件：第 " + str(row_num + 1) + " 行")


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
