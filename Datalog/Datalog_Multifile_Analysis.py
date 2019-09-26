# encoding:utf-8
# @Time     : 2019/9/11
# @Author   : Jerry Chou
# @File     :
# @Function : 1、多文件分析  2、根据需要的分组方式自动识别文件中分组

import pandas, os, math
import numpy as np
import datetime
from sys import argv

import xlwt

row_offset = 5
col_offset = 4


def find_item(list, value):
    '''
    找到value在list中所有的index
    :param list: 
    :param value: 
    :return: 
    '''
    return [i for i, v in enumerate(list) if v == value]

def get_nan_row(df):
    """
    获得有空值的行的列表
    :param df: 
    :return: 
    """
    exist_nan_row = df[df.isnull().T.any()]
    exist_nan_row_list = list(exist_nan_row.index.values)
    return exist_nan_row_list

def parse_file(file, group_by_id):
    try:
        read_file = pandas.read_csv(file, na_values=' ')
    except Exception as e:
        print(e)
    chipno_row_num = read_file[read_file.iloc[:, 0].isin(['ChipNo'])].index[0]
    group_name = read_file.iloc[chipno_row_num, group_by_id]
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

    ok_group_index = {}
    ok_group_list = read_file.iloc[ok_row_list, group_by_id]
    ok_group_int_list = [int(i) for i in ok_group_list]
    format_ok_group_list = list(set(ok_group_int_list))
    format_ok_group_list.sort()
    for i in format_ok_group_list:
        ok_group_index[i] = find_item(ok_group_int_list, i)
    # 遍历所有测试项
    for col_num in range(col_offset, read_file.shape[1] - 2):
        test_name = read_file.iloc[chipno_row_num, col_num]
        unit = read_file.iloc[chipno_row_num + 1, col_num]
        if isinstance(unit, float) and math.isnan(unit):
            unit = ''
        hi_limit = read_file.iloc[chipno_row_num + 2, col_num]
        lo_limit = read_file.iloc[chipno_row_num + 3, col_num]
        # 取得数据
        data = read_file.iloc[ok_row_list, col_num]
        temp = [test_name, unit, hi_limit, lo_limit]
        temp.append(cal_data(data, ok_group_index))
        # 计算数据
        result.append(temp)
    return result, format_ok_group_list, ok_group_index, group_name


def calc(data):
    min_value = data.min()
    max_value = data.max()
    std_value = np.std(data)
    mean_value = np.mean(data)

    # 付博观察值，>5%为异常值
    if mean_value != 0:
        std_div_mean = std_value / mean_value  # '{:.2%}'.format(std_value / mean_value)
    else:
        std_div_mean = 0
    return round(min_value, 6), round(mean_value, 6), round(max_value, 6), round(std_value, 6), round(std_div_mean, 6)


def cal_data(data, group_index):
    # 获取测试值，并转成float类型
    try:
        data_val = data.astype("float")
        calc_data = []
        for i in group_index:
            calc_data.append(calc(data_val.iloc[group_index[i]]))
    except Exception as e:
        print(e)

    return calc_data


def get_style(colour_id):
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be:NO_PATTERN,SOLID_PATTERN
    # May be: 0=Black,1=White,2=Red,3=Green,4=Blue,5=Yellow,6=Magenta,7=Cyan,
    # 16=Maroon,17=Dark Green,18=Dark Blue,19=Dark Yellow,20=Dark Megenta,
    # 21=Teal.22=Light Gray,23=Dark Gray
    pattern.pattern_fore_colour = colour_id
    style = xlwt.XFStyle()
    style.pattern = pattern
    return style


# 获取字符串长度，一个中文长度为2
def len_byte(value):
    length = len(str(value))
    uft8_length = len(value.encode('utf-8'))
    length = (uft8_length - length) / 2 + length
    return int(length)


def analysis_data(analysis_file, data):
    # 生成csv文件名拼接
    file_name = analysis_file.split('.')[0]
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")

    test_file_name = file_name + '_Analysis_by' + data[3] + '_' + date + '.xls'

    workbook = xlwt.Workbook(style_compression=2)

    line_sourcefile = ['Source file', analysis_file]
    line_title = ['TestName', 'Unit', 'LoLimit', 'HiLimit', 'Min', 'Mean', 'Max', 'std', 'StdDivMeanPercent']
    std_style = ['(1,10]', '(10,100]', '(100,+∞)']
    StdDivMeanPercent_style = ['[-50%,-5%),(5%,50%]', '[-500%,-50%),(50%,500%]', '(-∞,-500%),(500%,+∞)']

    for i in range(len(data[1])):
        worksheet = workbook.add_sheet(data[3] + str(data[1][i]))

        # 确定栏位宽度
        col_width = []
        col_num = 0
        for m in range(len(data[0])):
            col_num_tmp = 0
            for n in range(len(data[0][m]) - 1):
                if m == 0:
                    col_width.append(len_byte(data[0][m][n]))
                else:
                    if col_width[col_num_tmp] < len_byte(str(data[0][m][n])):
                        col_width[col_num_tmp] = len_byte(data[0][m][n])
                col_num_tmp += 1

            for x in range(len(data[0][m][4][i])):
                if m == 0:
                    col_width.append(len_byte(str(data[0][m][4][i][x])))
                else:
                    if col_width[col_num_tmp] < len_byte(str(data[0][m][4][i][x])):
                        col_width[col_num_tmp] = len_byte(str(data[0][m][4][i][x]))
                col_num_tmp += 1
            col_num = col_num_tmp
        for m in range(len(std_style)):
            if m == 0:
                col_width.append(len_byte(std_style[m]))
            else:
                if col_width[col_num] < len_byte(str(std_style[m])):
                    col_width[col_num] = len_byte(std_style[m])
        col_num += 1
        for m in range(len(StdDivMeanPercent_style)):
            if m == 0:
                col_width.append(len_byte(StdDivMeanPercent_style[m]))
            else:
                if col_width[col_num] < len_byte(str(StdDivMeanPercent_style[m])):
                    col_width[col_num] = len_byte(StdDivMeanPercent_style[m])
        if col_width[col_num] < len_byte(str(line_title[8])):
            col_width[col_num] = len_byte(line_title[8])

        col_num = 0
        for m in range(len(line_title)):
            if col_width[col_num] < len_byte(str(line_title[m])):
                col_width[col_num] = len_byte(line_title[m])
            col_num += 1

        # 设置栏位宽度，栏位宽度小于10时采用默认宽度
        for l in range(len(col_width)):
            if col_width[l] > 10:
                worksheet.col(l).width = 256 * (col_width[l] + 1)

        iRowIndex = 0
        worksheet.write(iRowIndex, 0, line_sourcefile[0])
        worksheet.write_merge(iRowIndex, 0, 1, 8, line_sourcefile[1])
        worksheet.write(iRowIndex, 9, line_title[7])
        worksheet.write(iRowIndex, 10, line_title[8])
        iRowIndex += 1
        worksheet.write(iRowIndex, 9, std_style[0], get_style(5))
        worksheet.write(iRowIndex, 10, StdDivMeanPercent_style[0], get_style(5))
        iRowIndex += 1
        worksheet.write(iRowIndex, 9, std_style[1], get_style(19))
        worksheet.write(iRowIndex, 10, StdDivMeanPercent_style[1], get_style(19))
        iRowIndex += 1
        worksheet.write(iRowIndex, 9, std_style[2], get_style(2))
        worksheet.write(iRowIndex, 10, StdDivMeanPercent_style[2], get_style(2))
        iRowIndex += 1
        line_loop_times = ['Test times', len(data[2][data[1][i]])]
        for index in range(len(line_loop_times)):
            worksheet.write(iRowIndex, index, line_loop_times[index])
        iRowIndex += 1
        for index in range(len(line_title)):
            worksheet.write(iRowIndex, index, line_title[index])
        iRowIndex += 1

        for j in range(len(data[0])):
            line = [data[0][j][0], data[0][j][1], data[0][j][3], data[0][j][2], data[0][j][4][i][0],
                    data[0][j][4][i][1], data[0][j][4][i][2], data[0][j][4][i][3], data[0][j][4][i][4]]
            for index in range(len(line)):
                if index == 7:
                    if 1 < line[index] <= 10:
                        worksheet.write(iRowIndex, index, line[index], get_style(5))
                    elif 10 < line[index] <= 100:
                        worksheet.write(iRowIndex, index, line[index], get_style(19))
                    elif 100 < line[index]:
                        worksheet.write(iRowIndex, index, line[index], get_style(2))
                    else:
                        worksheet.write(iRowIndex, index, line[index])
                elif index == 8:
                    if -0.5 <= line[index] < -0.05 or 0.05 < line[index] <= 0.5:
                        worksheet.write(iRowIndex, index, '{:.2%}'.format(line[index]), get_style(5))
                    elif -5 <= line[index] < -0.5 or 0.5 < line[index] <= 5:
                        worksheet.write(iRowIndex, index, '{:.2%}'.format(line[index]), get_style(19))
                    elif line[index] < -5 or 5 < line[index]:
                        worksheet.write(iRowIndex, index, '{:.2%}'.format(line[index]), get_style(2))
                    else:
                        worksheet.write(iRowIndex, index, '{:.2%}'.format(line[index]))
                else:
                    worksheet.write(iRowIndex, index, line[index])
            iRowIndex += 1
        # 设置第1列第6行窗口冻结
        worksheet.panes_frozen = True
        worksheet.vert_split_pos = 1
        worksheet.horz_split_pos = 6
    workbook.save(test_file_name)


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

    # Analysis folder path
    if argv.count('-a') == 0:
        analysis_folder = sourcefile_folder + '\Analysis'
    else:
        analysis_folder = argv[argv.index('-a') + 1]

    if argv.count('-b') == 0:
        group_by_id = 0  # 默认根据ChipNo分组
    else:
        group_by_id = int(argv[argv.index('-b') + 1])

    mkdir(analysis_folder)

    for file in file_list:
        original_file = os.path.join(sourcefile_folder, file)
        # parse file
        data = parse_file(original_file, group_by_id)

        analysis_file = os.path.join(analysis_folder, file)
        # analysis data
        analysis_data(analysis_file, data)


if __name__ == '__main__':
    main()
