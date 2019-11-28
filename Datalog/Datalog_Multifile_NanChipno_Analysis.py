# encoding:utf-8
# @Time     : 2019/9/11
# @Author   : Jerry Chou
# @File     :
# @Function : 1、多文件分析  2、分析空值的行

from csv import reader
from datetime import datetime
from os.path import dirname, basename, join, abspath
from os import getcwd
from sys import argv, path

path.append(abspath(join(getcwd(), '..')))
import Common

row_offset = 5
col_offset = 4


def parse_file(file):
    """
    解析文件
    :param file: 文件
    :return: dc空值chipno 和 image空值chipno
    """
    data = []
    with open(file) as f:
        csv_reader = reader(f)
        for row in csv_reader:
            data.append(row)

    search_pwdn_total = Common.search_string(data, 'PWDN_Total')
    if not search_pwdn_total:
        exit()
    else:
        pwdn_total_row_num = search_pwdn_total[0]
        pwdn_total_col_num = search_pwdn_total[1]

    search_binning = Common.search_string(data, 'Binning')
    if not search_binning:
        exit()
    else:
        binning_col_num = search_binning[1]

    col_count = binning_col_num + 1
    first_register_row_num = len(data) - 1
    for i in range(pwdn_total_row_num + row_offset, len(data)):
        try:
            int(data[i][0])
        except:
            first_register_row_num = i
            break
    dc_nan_chipno = []
    image_nan_chipno = []
    for i in range(pwdn_total_row_num + row_offset, first_register_row_num):
        for j in range(pwdn_total_col_num + 1):
            if len(data[i][j].strip()) == 0:
                dc_nan_chipno.append(data[i][0])
                break
    for i in range(pwdn_total_row_num + row_offset, first_register_row_num):
        for j in range(pwdn_total_col_num + 1, col_count):
            if len(data[i][j].strip()) == 0:
                image_nan_chipno.append(data[i][0])
                break

    return dc_nan_chipno, image_nan_chipno


def save_data(file, result_file, nan_chipno):
    """
    保存数据
    :param file: 解析文件路径
    :param result_file: 写结果文件
    :param nan_chipno: 空chipno列表
    :return: 
    """
    file_name = basename(file)
    with open(result_file, 'a') as f:
        f.write("            " + file_name + "：\n")
        if len(nan_chipno[0]) > 0 or len(nan_chipno[1]) > 0:
            if len(nan_chipno[0]) == 0:
                f.write("              (1) DC ：无空值\n")
            else:
                f.write("              (1) DC 共 " + str(len(nan_chipno[0])) + " 个，它们是:" + str(nan_chipno[0]) + "\n")
            if len(nan_chipno[1]) == 0:
                f.write("              (2) IMAGE ：无空值\n")
            else:
                f.write("              (2) IMAGE 共 " + str(len(nan_chipno[1])) + " 个，它们是:" + str(
                    nan_chipno[1]) + '\n')
        else:
            f.write("              没有空值。\n")


def main():
    # Sourcefile folder path
    if argv.count('-s') == 0 and argv.count('-f') == 0:
        print(
            "Error：Sourcefile folder path 或 single file path为必填项，格式：“-s D:\sourcefile” 或 “-f D:\sourcefile\ST5-440mm-out1.csv”。")
        exit()

    if argv.count('-s') != 0:
        sourcefile_folder = argv[argv.index('-s') + 1]
        file_list = Common.get_filelist(sourcefile_folder, '.csv')
        if not file_list:
            exit()

    if argv.count('-f') != 0:
        single_file = argv[argv.index('-f') + 1]
        sourcefile_folder = dirname(single_file)
        file_list = [single_file]

    # Analysis folder path
    if argv.count('-a') == 0:
        analysis_folder = sourcefile_folder + '\Analysis'
    else:
        analysis_folder = argv[argv.index('-a') + 1]

    Common.mkdir(analysis_folder)
    date = datetime.now().strftime("%Y%m%d%H%M")
    result_file = join(analysis_folder, 'NanChipno_Analysis' + date + '.txt')

    for file in file_list:
        # parse file
        nan_chipno = parse_file(file)
        # save data
        save_data(file, result_file, nan_chipno)


if __name__ == '__main__':
    main()
