# encoding:utf-8
# @Time     : 2019/9/17
# @Author   : Jerry Chou
# @File     :
# @Function : 多文件SWBIN分析

import pandas, os
import datetime
from sys import argv
import xlwt

row_offset = 5


def find_item(list, value):
    '''
    找到value在list中所有的index
    :param list: 
    :param value: 
    :return: 
    '''
    return [i for i, v in enumerate(list) if v == value]


def parse_file(file, group_by_id):
    try:
        read_file = pandas.read_csv(file)
    except Exception as e:
        print(e)
    chipno_row_num = read_file[read_file.iloc[:, 0].isin(['ChipNo'])].index[0]
    group_list = read_file.iloc[chipno_row_num + row_offset:, group_by_id]
    group_int_list = [int(i) for i in group_list]
    format_group_list = list(set(group_int_list))
    format_group_list.sort()

    group_index = {}
    for i in format_group_list:
        group_index[i] = find_item(group_int_list, i)

    file_name = os.path.basename(file).split('.')[0]
    return file_name, group_index


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


def analysis_data(analysis_folder, group_name, data):
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    test_file_name = analysis_folder + '/Analysis_by' + group_name + '_' + date + '.xls'
    workbook = xlwt.Workbook(style_compression=2)
    worksheet = workbook.add_sheet('Summary')
    worksheet.write(0, 0, group_name)

    sw_bin_list = [1, 2, 5, 6, 7, 9, 12, 13, 14, 15, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 40, 41, 42, 43,
                   44, 45, 53, 54, 55, 96, 97, 98, 99]

    # 确定栏位宽度
    col_width = []
    col_num = 0
    col_width.append(len_byte(group_name))
    col_num += 1
    for m in range(len(data)):
        col_width.append(len_byte(data[m][0] + '_COUNT'))
        col_num += 1

    # 设置栏位宽度，栏位宽度小于10时采用默认宽度
    for l in range(len(col_width)):
        if col_width[l] > 10:
            worksheet.col(l).width = 256 * (col_width[l] + 1)

    for i in range(len(data)):
        worksheet.write(0, 1 + i, data[i][0] + '_COUNT')
    for i in range(len(sw_bin_list)):
        worksheet.write(i + 1, 0, sw_bin_list[i])
        for j in range(len(data)):
            if sw_bin_list[i] in data[j][1]:
                bin_count = len(data[j][1][sw_bin_list[i]])
            else:
                bin_count = 0
            if j == 0:
                worksheet.write(i + 1, j + 1, bin_count)
            else:
                diff_count = bin_count - temp_count
                if diff_count > 0:
                    worksheet.write(i + 1, j + 1, str(bin_count) + '(+' + str(diff_count) + ')', get_style(2))
                elif diff_count == 0:
                    worksheet.write(i + 1, j + 1, str(bin_count) + '(-)')
                else:
                    worksheet.write(i + 1, j + 1, str(bin_count) + '(' + str(diff_count) + ')', get_style(5))
            temp_count = bin_count

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
        group_by_id = 2  # 默认根据SWBIN分组
    else:
        group_by_id = int(argv[argv.index('-b') + 1])

    if group_by_id == 0:
        group_name = 'ChipNo'
    elif group_by_id == 1:
        group_name = 'Site'
    elif group_by_id == 2:
        group_name = 'SWBIN'

    mkdir(analysis_folder)

    data = []
    for file in file_list:
        original_file = os.path.join(sourcefile_folder, file)
        # parse file
        data.append(parse_file(original_file, group_by_id))

    # analysis data
    analysis_data(analysis_folder, group_name, data)


if __name__ == '__main__':
    main()
