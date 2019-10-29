# encoding:utf-8
# @Time     : 2019/9/11
# @Author   : Jerry Chou
# @File     :
# @Function : 1、多文件分析  2、分析空值的行
import csv
import datetime
import os
from sys import argv

row_offset = 5
col_offset = 4
last_dc_testitem = 'PWDN_Total'

def parse_file(file, result_file):
    data = []
    with open(file) as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            data.append(row)
    for i in range(len(data)):
        try:
            pwdn_total_col_num = data[i].index(last_dc_testitem)
            pwdn_total_row_num = i
            break
        except:
            pass
    col_count = len(data[pwdn_total_row_num])
    firstregister_row_num = len(data)-1
    for i in range(pwdn_total_row_num + row_offset, len(data)):
        try:
            int(data[i][0])
        except:
            firstregister_row_num = i
            break
    dc_nan_chipno = []
    image_nan_chipno = []
    for i in range(pwdn_total_row_num + row_offset, firstregister_row_num):
        for j in range(pwdn_total_col_num + 1):
            if data[i][j].isspace():
                dc_nan_chipno.append(data[i][0])
                break
    for i in range(pwdn_total_row_num + row_offset, firstregister_row_num):
        for j in range(pwdn_total_col_num + 1, col_count - 4):
            if data[i][j].isspace():
                image_nan_chipno.append(data[i][0])
                break
    with open(result_file, 'a') as f:
        f.write(file + " 存在空值的chipno：\n")
        f.write("(1) DC 共 " + str(len(dc_nan_chipno)) + " 个，它们是:" + str(dc_nan_chipno) + "\n")
        f.write("(2) IMAGE 共 " + str(len(image_nan_chipno)) + " 个，它们是:" + str(image_nan_chipno) + '\n')

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
    result_file = os.path.join(analysis_folder, 'NanRow_Analysis' + date + '.txt')

    for file in file_list:
        original_file = os.path.join(sourcefile_folder, file)
        # parse file
        parse_file(original_file, result_file)


if __name__ == '__main__':
    main()
