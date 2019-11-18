# encoding:utf-8
# @Time     : 2019/9/17
# @Author   : Jerry Chou
# @File     :
# @Function : 多文件HWBIN、SWBIN分析
import csv

import os
import datetime
from sys import argv
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
from openpyxl.styles.colors import RED, YELLOW, GREEN, BLACK
from openpyxl.utils import get_column_letter

alignment = Alignment(horizontal='center', vertical='center')
thin = Side(border_style='thin', color=BLACK)
border = Border(top=thin, left=thin, right=thin, bottom=thin)

row_offset = 5


def find_item(list, value):
    '''
    找到value在list中所有的index
    :param list: 
    :param value: 
    :return: 
    '''
    return [i for i, v in enumerate(list) if v == value]


def sort_data(data):
    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            if len(data[i][1]) < len(data[j][1]):
                data[i], data[j] = data[j], data[i]


def parse_file(file, group_by_id):
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
    firstregister_row_num = len(data)
    for i in range(chipno_row_num + row_offset, len(data)):
        try:
            int(data[i][0])
        except:
            firstregister_row_num = i
            break
    group_list = []
    for i in range(chipno_row_num + row_offset, firstregister_row_num):
        group_list.append(int(data[i][group_by_id]))
    format_group_list = list(set(group_list))
    format_group_list.sort()

    group_index = []
    for i in format_group_list:
        temp = []
        temp.append(i)
        data_list = find_item(group_list, i)
        if group_by_id == 1:
            temp_list = []
            for j in data_list:
                temp_list.append(data[chipno_row_num + row_offset + j][2])
            format_temp_list = list(set(temp_list))
            temp_index = []
            for m in format_temp_list:
                temp_swbin = [m]
                temp_data_list = find_item(temp_list, m)
                temp_swbin.append(temp_data_list)
                temp_index.append(temp_swbin)
            temp.append(temp_index)
        else:
            temp.append(data_list)
        group_index.append(temp)

    file_name = os.path.basename(file).split('.')[0]
    group_name = data[chipno_row_num][group_by_id]
    lotno = data[5][1]
    return file_name, group_index, group_name, lotno


def set_column_width(sheet):
    # 获取每一列的内容的最大宽度
    col_width = [0.5] * sheet.max_column
    for row in range(sheet.max_row):
        for col in range(sheet.max_column):
            value = sheet.cell(row=row + 1, column=col + 1).value
            if value:
                width = len(str(value))
                if width > col_width[col]:
                    col_width[col] = width
    # 设置列宽
    for i in range(len(col_width)):
        col_lettert = get_column_letter(i + 1)
        if col_width[i] > 100:
            sheet.column_dimensions[col_lettert].width = 100
        else:
            sheet.column_dimensions[col_lettert].width = col_width[i] + 2


def analysis_data(analysis_folder, site_data, softbin_data, hardbin_data):
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    test_file_name = analysis_folder + '/Summary_Analysis_' + date + '.xlsx'
    wb = Workbook()

    bin_list = [
        [1, [1, 2]],
        [2, [41, 42, 43, 44, 45, 53, 54, 55]],
        [4, [23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 36, 39, 40, 70, 71, 72]],
        [5, [5, 6, 7, 8, 9, 12, 96, 97, 98, 99]],
        [6, [13, 14, 15, 35]]
    ]
    hardbin_sheet = wb.create_sheet('HWBin')
    hardbin_sheet.freeze_panes = 'B1'
    iRow = 1
    hardbin_sheet.cell(row=iRow, column=1).value = 'File'
    for i in range(len(bin_list)):
        hardbin_sheet.cell(row=iRow, column=(2 + i)).value = 'HWBin' + str(bin_list[i][0])
    hardbin_sheet.cell(row=iRow, column=7).value = 'TestCount'
    hardbin_sheet.cell(row=iRow, column=8).value = 'PassPercent'
    iRow += 1
    summary_data = []
    for i in range(len(hardbin_data)):
        temp_list = []
        temp_list.append(hardbin_data[i][0])
        test_count = 0
        pass_count = len(hardbin_data[i][1][0][1])+len(hardbin_data[i][1][1][1])
        for hw_bin in bin_list:
            for j in range(len(hardbin_data[i][1])):
                if hw_bin[0] == hardbin_data[i][1][j][0]:
                    bin_count = len(hardbin_data[i][1][j][1])
                    break
                else:
                    bin_count = 0
            test_count += bin_count
            temp_list.append(bin_count)
        temp_list.append(test_count)
        pass_percent = '{:.2%}'.format(pass_count / test_count)
        temp_list.append(pass_percent)
        summary_data.append(temp_list)

    for i in range(len(summary_data)):
        for j in range(len(summary_data[i])):
            hardbin_sheet.cell(row=iRow, column=(j + 1)).value = summary_data[i][j]
            if 1 <= j <= 5:
                hardbin_sheet.cell(row=iRow + 1, column=(j + 1)).value = '{:.2%}'.format(summary_data[i][j]/summary_data[i][6])
                hardbin_sheet.cell(row=iRow + 1, column=(j + 1)).fill = PatternFill(fill_type='solid', fgColor=GREEN)
        iRow += 2
    hardbin_sheet.cell(row=iRow, column=1).value = 'Summary'
    summary_bin1_count = 0
    summary_bin2_count = 0
    for i in range(len(summary_data)):
        summary_bin1_count += summary_data[i][1]
        summary_bin2_count += summary_data[i][2]
    ok_bin_count = summary_bin1_count + summary_bin2_count
    hardbin_sheet.cell(row=iRow, column=2).value = summary_bin1_count
    hardbin_sheet.cell(row=iRow, column=3).value = summary_bin2_count
    for i in range(3, len(summary_data[-1]) - 2):
        hardbin_sheet.cell(row=iRow, column=(i + 1)).value = summary_data[-1][i]
    hardbin_sheet.cell(row=iRow, column=7).value = summary_data[0][6]
    hardbin_sheet.cell(row=iRow, column=8).value = '{:.2%}'.format(ok_bin_count / summary_data[0][6])

    for row in hardbin_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1:
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                cell.font = Font(bold=True)
                cell.alignment = alignment
            if cell.row == 2 and cell.column == hardbin_sheet.max_column:
                cell.fill = PatternFill(fill_type='solid', fgColor=GREEN)
            if cell.row == hardbin_sheet.max_row and cell.column == hardbin_sheet.max_column:
                cell.fill = PatternFill(fill_type='solid', fgColor=GREEN)

    hardsoftbin_sheet = wb.create_sheet('HWBin-SWBin')
    hardsoftbin_sheet.freeze_panes = 'C2'
    iRow = 1
    hardsoftbin_sheet.cell(row=iRow, column=1).value = softbin_data[0][3]
    hardsoftbin_sheet.cell(row=iRow, column=3).value = 'FT'
    for i in range(1, len(softbin_data)):
        hardsoftbin_sheet.cell(row=iRow, column=3 + i).value = 'RT' + str(i)
    iRow += 1

    swbin_sort_by_FT_list = []
    for i in range(len(bin_list)):
        temp_list = []
        for j in range(len(bin_list[i][1])):
            find_softbin = False
            for x in range(len(softbin_data[0][1])):
                if bin_list[i][1][j] == softbin_data[0][1][x][0]:
                    find_softbin = True
                    len1 = len(softbin_data[0][1][x][1])
                    temp_list.append((j, len1))
            if not find_softbin:
                temp_list.append((j, 0))
        for m in range(len(temp_list) - 1):
            for n in range(m + 1, len(temp_list)):
                if temp_list[m][1] < temp_list[n][1]:
                    temp_list[m], temp_list[n] = temp_list[n], temp_list[m]
        temp_count_list = [bin_list[i][0]]
        for y in range(len(temp_list)):
            temp_count_list.append(bin_list[i][1][temp_list[y][0]])
        swbin_sort_by_FT_list.append(temp_count_list)

    for i in range(len(swbin_sort_by_FT_list)):
        hardsoftbin_sheet.cell(row=iRow, column=1).value = 'HWBin' + str(swbin_sort_by_FT_list[i][0])
        hardsoftbin_sheet.cell(row=iRow, column=1).fill = PatternFill(fill_type='solid', fgColor=GREEN)
        hardsoftbin_sheet.cell(row=iRow, column=1).font = Font(bold=True)
        for j in range(1, len(swbin_sort_by_FT_list[i])):
            hardsoftbin_sheet.cell(row=iRow, column=2).value = 'SWBin' + str(swbin_sort_by_FT_list[i][j])
            for m in range(len(softbin_data)):
                for n in range(len(softbin_data[m][1])):
                    if swbin_sort_by_FT_list[i][j] == softbin_data[m][1][n][0]:
                        hardsoftbin_sheet.cell(row=iRow, column=(3 + m)).value = len(softbin_data[m][1][n][1])
            iRow += 1
        iRow += 1
    for row in hardsoftbin_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1:
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                cell.font = Font(bold=True)
                cell.alignment = alignment

    for sheet_name in wb.sheetnames:
        if sheet_name == 'Sheet':
            del wb[sheet_name]
        else:
            set_column_width(wb[sheet_name])

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

    # Analysis folder path
    if argv.count('-a') == 0:
        analysis_folder = sourcefile_folder + '\Analysis'
    else:
        analysis_folder = argv[argv.index('-a') + 1]

    mkdir(analysis_folder)

    hardbin_data = []
    softbin_data = []
    site_data = []
    for file in file_list:
        original_file = os.path.join(sourcefile_folder, file)
        # parse file
        site_data.append(parse_file(original_file, 1))
        softbin_data.append(parse_file(original_file, 2))
        hardbin_data.append(parse_file(original_file, 3))

    for data in softbin_data:
        sort_data(data[1])

    # analysis data
    analysis_data(analysis_folder, site_data, softbin_data, hardbin_data)


if __name__ == '__main__':
    main()
