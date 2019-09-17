# encoding:utf-8
# @Time     : 2019/9/9 13:32
# @Author   : Jerry Chou
# @File     :
# @Function :

import pandas, os
import numpy as np
import csv
import datetime, math
from sys import argv

row_offset = 5
col_offset = 4

def parse_golden_data_file(file):
    read_file = pandas.read_csv(file)
    chipno_line_num = read_file[read_file.iloc[:, 0].isin(['ChipNo'])].index[0]
    three_sigma_low_end_list = ['3SigmaLowEnd', '', '', '']
    three_sigma_high_end_list = ['3SigmaHighEnd', '', '', '']
    for col_num in range(col_offset, read_file.shape[1] - 2):
        data = read_file.iloc[chipno_line_num + row_offset:, col_num].astype("float")
        std_value = np.std(data)
        mean_value = np.mean(data)
        # 平均值：
        # 对于高斯分布的数据来说，68.27%的数据集集中在一个标准差的范围内，95.45%在两个标准差的范围内，
        # 99.73%在三个标准差的范围内，因此根据这个，和平均值相差3倍标准差的点被看作异常点，
        # 但平均数和标准差太容易受异常点干扰，其有限样本击穿点是0%
        # 平均值上下三倍标准差之间属于正常点
        three_sigma_low_end = mean_value - 3 * std_value
        three_sigma_high_end = mean_value + 3 * std_value
        three_sigma_high_end_list.append(three_sigma_high_end)
        three_sigma_low_end_list.append(three_sigma_low_end)
    return three_sigma_low_end_list, three_sigma_high_end_list


def parse_file(file, golden_data):
    read_file = pandas.read_csv(file)
    chipno_line_num = read_file[read_file.iloc[:, 0].isin(['ChipNo'])].index[0]
    result = []
    for row_num in range(read_file.shape[0]):
        row_data = []
        for col_num in range(read_file.shape[1] - 2):
            value = read_file.iloc[row_num, col_num]
            if row_num >= chipno_line_num + row_offset and col_num >= col_offset:
                try:
                    value_float = float(value)
                except Exception as e:
                    print(e)
                if golden_data[0][col_num] <= value_float <= golden_data[1][col_num]:
                    row_data.append('')
                else:
                    row_data.append(value)
            else:
                if isinstance(value, float) and math.isnan(value):
                    value = ''
                row_data.append(value)
        result.append(row_data)
    return result


def analysis_data(file, golden_data, data):
    file_name = file.split('.')[0]
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    test_file_name = file_name + ' vs GoldenData_' + date + '.csv'

    with open(test_file_name, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for index, line in enumerate(data):
            if index == 14:
                writer.writerow(golden_data[1])
                writer.writerow(golden_data[0])
            writer.writerow(line)


def mkdir(dir):
    dir = dir.strip()
    dir = dir.rstrip("\\")
    isExists = os.path.exists(dir)
    if not isExists:
        os.makedirs(dir)
        # print(path + '创建成功')
        return True
    else:
        # print(path + '目录已存在')
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

    # Golden data file path
    if argv.count('-g') == 0:
        print("Error：Golden data file path为必填项，格式：“-g D:\cBin1 16ea.csv”。")
        exit()
    else:
        golden_data_file = argv[argv.index('-g') + 1]

    # Analysis folder path
    if argv.count('-a') == 0:
        analysis_folder = sourcefile_folder + '\Analysis'
    else:
        analysis_folder = argv[argv.index('-a') + 1]

    golden_data = parse_golden_data_file(golden_data_file)
    mkdir(analysis_folder)

    for file in file_list:
        original_file = os.path.join(sourcefile_folder, file)
        # parse file
        data = parse_file(original_file, golden_data)

        analysis_file = os.path.join(analysis_folder, file)
        # analysis data
        analysis_data(analysis_file, golden_data, data)


if __name__ == '__main__':
    main()
