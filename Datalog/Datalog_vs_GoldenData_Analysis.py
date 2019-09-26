# encoding:utf-8
# @Time     : 2019/9/9 13:32
# @Author   : Jerry Chou
# @File     :
# @Function :

import pandas, os
import numpy as np
import datetime, math
from sys import argv

from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side

row_offset = 5
col_offset = 4

golden_data_color = '00FFFF'  # 水绿色


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

def get_nan_row(df):
    """
    获得有空值的行的列表
    :param df: 
    :return: 
    """
    exist_nan_row = df[df.isnull().T.any()]
    exist_nan_row_list = list(exist_nan_row.index.values)
    return exist_nan_row_list

def parse_file(file, golden_data):
    read_file = pandas.read_csv(file)
    chipno_line_num = read_file[read_file.iloc[:, 0].isin(['ChipNo'])].index[0]
    try:
        read_file = pandas.read_csv(file, na_values=' ')
    except Exception as e:
        print(e)
    chipno_row_num = read_file[read_file.iloc[:, 0].isin(['ChipNo'])].index[0]
    chipnum_df = read_file.iloc[chipno_row_num + row_offset:, 0]
    for chipnum in chipnum_df:
        try:
            int(chipnum)
        except:
            FirstRegister = chipnum
            break
    firstregister_row_num = read_file[read_file.iloc[:, 0].isin([FirstRegister])].index[0]
    result = []

    whole_data_df = read_file.iloc[chipno_row_num + row_offset:firstregister_row_num, 0:read_file.shape[1] - 2]
    exist_nan_row_list = get_nan_row(whole_data_df)

    data_row_list = range(chipno_row_num + row_offset, firstregister_row_num)
    ok_row_list = list(set(data_row_list) - set(exist_nan_row_list))
    for row_num in range(read_file.shape[0]):
        row_data = []
        for col_num in range(read_file.shape[1] - 2):
            value = read_file.iloc[row_num, col_num]
            if chipno_line_num + 2 <= row_num <= chipno_line_num + 3:
                row_data.append((value, '008000'))  # 纯绿
            elif row_num in ok_row_list and col_num >= col_offset:
                high_limit_data = read_file.iloc[chipno_line_num + 2, col_num]
                if high_limit_data == ' ' or high_limit_data == 'N':
                    high_limit = ''
                else:
                    high_limit = float(high_limit_data)
                low_limit_data = read_file.iloc[chipno_line_num + 3, col_num]
                if low_limit_data == ' ' or low_limit_data == 'N':
                    low_limit = ''
                else:
                    low_limit = float(low_limit_data)
                try:
                    value_float = float(value)
                    if golden_data[0][col_num] <= value_float <= golden_data[1][col_num]:
                        row_data.append((value, 'FFFFFF'))  # 白色
                    elif high_limit != '' and (low_limit <= value_float < golden_data[0][col_num] or golden_data[1][
                        col_num] < value_float <= high_limit):
                        row_data.append((value, 'FFFF00'))  # 纯黄
                    else:
                        row_data.append((value, 'FF0000'))  # 纯红
                except Exception as e:
                    print(e)
            elif chipno_row_num + row_offset<=row_num<firstregister_row_num and row_num not in ok_row_list:
                row_data.append((value,'A020F0')) # purple
            else:
                if isinstance(value, float) and math.isnan(value):
                    value = ''
                row_data.append((value, 'FFFFFF'))
        result.append(row_data)
    return result


def analysis_data(file, data, golden_data):
    file_name = file.split('.')[0]
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    test_file_name = file_name + ' vs GoldenData_' + date + '.xlsx'

    wb = Workbook()  # 创建文件对象

    ws = wb.active  # 获取第一个sheet
    ws.freeze_panes = 'E18'

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
        irow += 1
    wb.save(test_file_name)


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
        analysis_data(analysis_file, data, golden_data)


if __name__ == '__main__':
    main()
