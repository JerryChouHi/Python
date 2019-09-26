# encoding:utf-8
# @Time     : 2019/9/17
# @Author   : Jerry Chou
# @File     :
# @Function : 多文件HWBIN分析

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
    chipnum_df = read_file.iloc[chipno_row_num + row_offset:, 0]
    for chipnum in chipnum_df:
        try:
            int(chipnum)
        except:
            FirstRegister = chipnum
            break
    firstregister_row_num = read_file[read_file.iloc[:, 0].isin([FirstRegister])].index[0]
    group_list = read_file.iloc[chipno_row_num + row_offset:firstregister_row_num, group_by_id]
    group_int_list = [int(i) for i in group_list]
    format_group_list = list(set(group_int_list))
    format_group_list.sort()

    group_index = {}
    for i in format_group_list:
        group_index[i] = find_item(group_int_list, i)

    file_name = os.path.basename(file).split('.')[0]
    group_name = read_file.iloc[chipno_row_num, group_by_id]
    return file_name, group_index, group_name


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


def analysis_data(analysis_folder, data):
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    test_file_name = analysis_folder + '/Analysis_by' + data[0][2] + '_' + date + '.xls'
    workbook = xlwt.Workbook(style_compression=2)
    worksheet = workbook.add_sheet('Summary')
    hw_bin_list = [1, 2, 3, 4, 5, 6]
    iRow = 0
    worksheet.write(iRow, 0, 'File')
    for i in range(len(hw_bin_list)):
        worksheet.write(iRow, 1 + i, 'HWBin' + str(hw_bin_list[i]))
    worksheet.write(iRow, 7, '测试数量')
    worksheet.write(iRow, 8, '良率')
    iRow += 1
    summary_data = []
    col_width = []
    for i in range(len(data)):
        temp_list = []
        temp_list.append(data[i][0])
        if i==0:
            col_width.append(len_byte(data[i][0]))
        else:
            if col_width[0] < len_byte(str(data[i][0])):
                col_width[0] = len_byte(data[i][0])
        test_count = 0
        pass_count = len(data[i][1][1])
        for j in range(len(hw_bin_list)):
            if hw_bin_list[j] in data[i][1]:
                bin_count = len(data[i][1][hw_bin_list[j]])
            else:
                bin_count = 0
            test_count += bin_count
            temp_list.append(bin_count)
        temp_list.append(test_count)
        pass_percent = '{:.2%}'.format(pass_count / test_count)
        temp_list.append(pass_percent)
        summary_data.append(temp_list)

    # 设置栏位宽度，栏位宽度小于10时采用默认宽度
    for i in range(len(col_width)):
        if col_width[i] > 10:
            worksheet.col(i).width = 256 * (col_width[i] + 1)


    for i in range(len(summary_data)):
        for j in range(len(summary_data[i])):
            worksheet.write(iRow, j, summary_data[i][j])
        iRow += 1
    worksheet.write(iRow, 0, 'Summary',get_style(5))
    summary_bin1_count = 0
    for i in range(len(summary_data)):
        summary_bin1_count += summary_data[i][1]
    worksheet.write(iRow, 1, summary_bin1_count)
    for i in range(2, len(summary_data[-1])-2):
        worksheet.write(iRow, i, summary_data[-1][i])
    worksheet.write(iRow, 7, summary_data[0][7])
    worksheet.write(iRow, 8, '{:.2%}'.format(summary_bin1_count / summary_data[0][7]),get_style(5))
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
        group_by_id = 3  # 默认根据HWBIN分组
    else:
        group_by_id = int(argv[argv.index('-b') + 1])

    mkdir(analysis_folder)

    data = []
    for file in file_list:
        original_file = os.path.join(sourcefile_folder, file)
        # parse file
        data.append(parse_file(original_file, group_by_id))

    # analysis data
    analysis_data(analysis_folder, data)


if __name__ == '__main__':
    main()
