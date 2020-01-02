# encoding:utf-8
# @Time     : 2019/9/10
# @Author   : Jerry Chou
# @File     :
# @Function :

from csv import reader
from os import listdir, makedirs
from os.path import join, isdir, exists, basename, dirname
import numpy as np
import csv
from datetime import datetime
from sys import argv


def search_string(data, target):
    """
    查找字符串
    :param data: 数据
    :param target: 待查找字符串
    :return: 行、列
    """
    for i in range(len(data)):
        try:
            col_num = data[i].index(target)
            row_num = i
            return row_num, col_num
        except:
            pass
    print("没有找到 " + target + " ！")
    return False


def parse_file(file):
    # 拼接文件名
    print(file + ":解析文件开始>>>>>>>>>>>>")
    data = []
    with open(file) as f:
        csv_reader = reader(f)
        for row in csv_reader:
            data.append(row)
    SearchTriggerCount = search_string(data, 'Trigger count')
    if not SearchTriggerCount:
        exit()
    else:
        TriggerCountRowNum = SearchTriggerCount[0]
    result = []
    for row_num in range(TriggerCountRowNum + 1, len(data)):
        if row_num == 0:
            if data[row_num][2] == 'GO':
                group_start_row_num = row_num
        else:
            if data[row_num - 1][2] != 'GO' and data[row_num][2] == 'GO':
                group_start_row_num = row_num
            if data[row_num - 1][2] == 'GO' and data[row_num][2] != 'GO':
                group_end_row_num = row_num
                result.append(cal_data(data, group_start_row_num, group_end_row_num))
    if data[TriggerCountRowNum + 1][2] == 'GO':
        del result[0]

    max_list = []
    for item in result:
        max_list.append(item[1])
    min = np.min(max_list)
    max = np.max(max_list)
    mean = np.mean(max_list)
    std = np.std(max_list)
    six_sigma = 6 * std
    cp20 = 40 / six_sigma
    cp15 = 30 / six_sigma
    print(file + ":解析文件结束<<<<<<<<<<<")
    return result, min, max, mean, six_sigma, cp20, cp15


def cal_data(data, row_num1, row_num2):
    max_value = float(data[row_num1][1])
    trigger_count = data[row_num1][0]
    for row_num in range(row_num1 + 1, row_num2):
        if float(data[row_num][1]) > max_value:
            max_value = float(data[row_num][1])
            trigger_count = data[row_num][0]
    return trigger_count, max_value * 1000


def analysis_data(analysis_file, data):
    with open(analysis_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['trigger count', 'OUT(um)', '', 'min', 'max', 'average', '6 sigma', 'cp(20um)', 'cp(15um)'])
        for i in range(len(data[0])):
            line = [data[0][i][0], data[0][i][1]]
            if i == 0:
                line.extend(['', data[1], data[2], data[3], data[4], data[5], data[6]])
            writer.writerow(line)
    print(analysis_file + ":写文件结束<<<<<<<<<<<")


def mkdir(dir):
    dir = dir.strip()
    dir = dir.rstrip("\\")
    isExists = exists(dir)
    if not isExists:
        makedirs(dir)
        return True
    else:
        return False


def get_filelist(folder, postfix=None):
    """
    获取某个后缀的文件列表
    :param postfix: 后缀，默认为None
    :param folder: 文件夹路径
    :return: 文件列表
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
        print("Error：不是文件夹！")
        return False


def main():
    # Sourcefile folder path
    if argv.count('-s') == 0 and argv.count('-f') == 0:
        print(
            "Error：Sourcefile folder path 或 single file path为必填项，格式：“-s D:\sourcefile” 或 “-f D:\sourcefile\ST5-440mm-out1.csv”。")
        exit()

    if argv.count('-s') != 0:
        sourcefile_folder = argv[argv.index('-s') + 1]
        file_list = get_filelist(sourcefile_folder, '.csv')
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

    mkdir(analysis_folder)

    for file in file_list:
        # parse file
        data = parse_file(file)

        # 生成csv文件名拼接
        file_name = basename(file).split('.')[0]
        date = datetime.now().strftime("%Y%m%d%H%M")
        analysis_file = join(analysis_folder, file_name + '_Analysis' + date + '.csv')
        print(analysis_file + ":写文件开始>>>>>>>>>>>>")

        # analysis data
        analysis_data(analysis_file, data)


if __name__ == '__main__':
    main()
