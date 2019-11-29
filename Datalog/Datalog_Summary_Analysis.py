# encoding:utf-8
# @Time     : 2019/9/17
# @Author   : Jerry Chou
# @File     :
# @Function : 多文件HWBIN、SWBIN分析

from csv import reader
from os.path import basename, dirname, abspath, join
from os import getcwd
from datetime import datetime
from sys import argv, path
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
from openpyxl.styles.colors import YELLOW, GREEN, BLACK, WHITE, RED

path.append(abspath(join(getcwd(), '..')))
import Common

alignment = Alignment(horizontal='center', vertical='center')
thin = Side(border_style='thin', color=BLACK)
border = Border(top=thin, left=thin, right=thin, bottom=thin)

row_offset = 5


def parse_file(file, group_by_id):
    """
    解析文件
    :param file: datalog csv文件
    :param group_by_id: 列序号（1：Site，2：SW_BIN，3：hW_BIN）
    :return: 文件名，分组index列表，分组名，lotno
    """
    data = []
    with open(file) as f:
        csv_reader = reader(f)
        for row in csv_reader:
            data.append(row)
    for i in range(len(data)):
        try:
            data[i].index('ChipNo')
            chipno_row_num = i
            break
        except:
            pass
    first_register_row_num = len(data) - 1
    for i in range(chipno_row_num + row_offset, len(data)):
        try:
            int(data[i][0])
        except:
            first_register_row_num = i
            break
    group_list = []
    for i in range(chipno_row_num + row_offset, first_register_row_num):
        group_list.append(int(data[i][group_by_id]))
    format_group_list = list(set(group_list))
    format_group_list.sort()

    group_index = []
    for i in format_group_list:
        temp = []
        temp.append(i)
        data_list = Common.find_item(group_list, i)
        if group_by_id == 1:
            temp_list = []
            for j in data_list:
                temp_list.append(data[chipno_row_num + row_offset + j][2])
            format_temp_list = list(set(temp_list))
            temp_index = []
            for m in format_temp_list:
                temp_swbin = [m]
                temp_data_list = Common.find_item(temp_list, m)
                temp_swbin.append(temp_data_list)
                temp_index.append(temp_swbin)
            temp.append(temp_index)
        else:
            temp.append(data_list)
        group_index.append(temp)

    file_name = basename(file).split('.')[0]
    group_name = data[chipno_row_num][group_by_id]
    lotno = data[5][1]
    return file_name, group_index, group_name, lotno


def save_data(analysis_folder, site_data, softbin_data, hardbin_data):
    """
    写数据
    :param analysis_folder: 保存分析文件夹路径
    :param site_data: site数据
    :param softbin_data: softbin数据
    :param hardbin_data: hardbin数据
    :return: 
    """
    date = datetime.now().strftime("%Y%m%d%H%M")
    test_file_name = analysis_folder + '/Summary_Analysis_' + date + '.xlsx'
    wb = Workbook()

    bin_list = [
        [1, [1, 2]],
        [2, [41, 42, 43, 44, 45, 53, 54, 55]],
        [4, [23, 24, 25, 29, 30, 33, 34, 36, 39, 40, 70, 71, 72]],
        [5, [5, 6, 7, 8, 9, 12, 96, 97, 98, 99]],
        [6, [13, 14, 15, 35]],
        [8, [26, 27, 31, 32]]  # 专门分出来测试良率
    ]
    hardbin_sheet = wb.create_sheet('HWBin')
    hardbin_sheet.freeze_panes = 'B2'
    summary_data = []
    for i in range(len(hardbin_data)):
        temp_list = []
        if i == 0:
            temp_list.append('FT')
        else:
            temp_list.append('RT' + str(i))
        test_count = 0
        pass_count = len(hardbin_data[i][1][0][1]) + len(hardbin_data[i][1][1][1])
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
    irow = 1
    icol = 1
    hardbin_sheet.cell(row=irow, column=icol).value = softbin_data[0][3]
    icol += 1
    for i in range(len(bin_list)):
        hardbin_sheet.cell(row=irow, column=icol).value = 'HWBin' + str(bin_list[i][0])
        icol += 1
    hardbin_sheet.cell(row=irow, column=icol).value = 'TestCount'
    icol += 1
    hardbin_sheet.cell(row=irow, column=icol).value = 'PassPercent'
    irow += 1
    for i in range(len(summary_data)):
        for j in range(len(summary_data[i])):
            hardbin_sheet.cell(row=irow, column=(j + 1)).value = summary_data[i][j]
            if j == 0:
                hardbin_sheet.cell(row=irow, column=(j + 1)).fill = PatternFill(fill_type='solid', fgColor=GREEN)
            if 1 <= j < len(summary_data[i]) - 2:
                hardbin_sheet.cell(row=irow + 1, column=(j + 1)).value = '{:.2%}'.format(
                    summary_data[i][j] / summary_data[i][-2])
                hardbin_sheet.cell(row=irow + 1, column=(j + 1)).fill = PatternFill(fill_type='solid', fgColor=GREEN)
        irow += 2
    hardbin_sheet.cell(row=irow, column=1).value = 'Summary'
    hardbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=GREEN)
    summary_bin1_count = 0
    summary_bin2_count = 0
    for i in range(len(summary_data)):
        summary_bin1_count += summary_data[i][1]
        summary_bin2_count += summary_data[i][2]
    ok_bin_count = summary_bin1_count + summary_bin2_count
    hardbin_sheet.cell(row=irow, column=2).value = summary_bin1_count
    hardbin_sheet.cell(row=irow, column=3).value = summary_bin2_count
    for i in range(3, len(summary_data[-1]) - 2):
        hardbin_sheet.cell(row=irow, column=(i + 1)).value = summary_data[-1][i]
    hardbin_sheet.cell(row=irow, column=icol - 1).value = summary_data[0][-2]
    hardbin_sheet.cell(row=irow, column=icol).value = '{:.2%}'.format(ok_bin_count / summary_data[0][-2])

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
    irow = 1
    hardsoftbin_sheet.cell(row=irow, column=1).value = softbin_data[0][3]
    hardsoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
    hardsoftbin_sheet.cell(row=irow, column=3).value = 'FT'
    hardsoftbin_sheet.cell(row=irow, column=3).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
    hardsoftbin_sheet.merge_cells(start_row=irow, end_row=irow, start_column=3, end_column=4)
    for i in range(1, len(softbin_data)):
        hardsoftbin_sheet.cell(row=irow, column=3 + 2 * i).value = 'RT' + str(i)
        hardsoftbin_sheet.cell(row=irow, column=3 + 2 * i).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
        hardsoftbin_sheet.merge_cells(start_row=irow, end_row=irow, start_column=3 + 2 * i, end_column=4 + 2 * i)
    irow += 1

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

    summary_soft_count = []
    for i in range(len(swbin_sort_by_FT_list)):
        hardsoftbin_sheet.cell(row=irow, column=1).value = 'HWBin' + str(swbin_sort_by_FT_list[i][0])
        hardsoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=GREEN)
        hardsoftbin_sheet.cell(row=irow, column=1).font = Font(bold=True)
        for j in range(1, len(swbin_sort_by_FT_list[i])):
            hardsoftbin_sheet.cell(row=irow, column=2).value = 'SWBin' + str(swbin_sort_by_FT_list[i][j])
            temp_count = 0
            for m in range(len(softbin_data)):
                find_softbin = False
                for n in range(len(softbin_data[m][1])):
                    if swbin_sort_by_FT_list[i][j] == softbin_data[m][1][n][0]:
                        find_softbin = True
                        swbin_count = len(softbin_data[m][1][n][1])
                if not find_softbin:
                    swbin_count = 0
                if i in (0, 1):
                    temp_count += swbin_count
                elif m == len(softbin_data) - 1:
                    temp_count = swbin_count
                hardsoftbin_sheet.cell(row=irow, column=(2 * m + 3)).value = swbin_count
                hardsoftbin_sheet.cell(row=irow, column=(2 * m + 4)).value = '{:.2%}'.format(
                    swbin_count / summary_data[0][-2])  # 当次测试总数 summary_data[m][6])
                hardsoftbin_sheet.cell(row=irow, column=(2 * m + 4)).fill = PatternFill(fill_type='solid',
                                                                                        fgColor=GREEN)
            irow += 1
            summary_soft_count.append(temp_count)
        summary_soft_count.append('')
        irow += 1

    irow = 1
    icol = 4 + 2 * len(softbin_data)
    hardsoftbin_sheet.cell(row=irow, column=icol).value = 'Summary'
    hardsoftbin_sheet.cell(row=irow, column=icol).fill = PatternFill(fill_type='solid', fgColor='FFA500')
    hardsoftbin_sheet.merge_cells(start_row=irow, end_row=irow, start_column=icol, end_column=icol + 1)
    irow += 1
    for i in range(len(summary_soft_count)):
        if isinstance(summary_soft_count[i], int):
            hardsoftbin_sheet.cell(row=irow, column=icol).value = summary_soft_count[i]
            hardsoftbin_sheet.cell(row=irow, column=icol + 1).value = '{:.2%}'.format(
                summary_soft_count[i] / summary_data[0][-2])
            hardsoftbin_sheet.cell(row=irow, column=icol + 1).fill = PatternFill(fill_type='solid', fgColor='FFA500')
        irow += 1

    for row in hardsoftbin_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1:
                cell.font = Font(bold=True)
                cell.alignment = alignment

    bin_list = [1, 2, 41, 42, 43, 44, 45, 53, 54, 55, 23, 24, 25, 29, 30, 33, 34, 36, 39, 40, 70, 71,
                72, 5, 6, 7, 8, 9, 12, 96, 97, 98, 99, 13, 14, 15, 35, 26, 27, 31, 32]
    sitesoftbin_sheet = wb.create_sheet('Site-SWBin')
    sitesoftbin_sheet.freeze_panes = 'B2'
    irow = 1
    sitesoftbin_sheet.cell(row=irow, column=1).value = site_data[0][3]
    sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
    for i in range(len(site_data[0][1])):
        sitesoftbin_sheet.cell(row=irow, column=2 + i).value = 'Site' + str(site_data[0][1][i][0])
        sitesoftbin_sheet.cell(row=irow, column=2 + i).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
    sitesoftbin_sheet.cell(row=irow, column=3 + len(site_data[0][1])).value = 'Summary'
    sitesoftbin_sheet.cell(row=irow, column=3 + len(site_data[0][1])).fill = PatternFill(fill_type='solid',
                                                                                         fgColor='FFA500')
    irow += 1

    site_swbin_percent = []
    for x in range(len(bin_list)):
        temp_list = []
        temp_total_count = 0
        for i in range(len(site_data[0][1])):
            find_softbin = False
            for j in range(len(site_data[0][1][i][1])):
                if bin_list[x] == int(site_data[0][1][i][1][j][0]):
                    temp_swbin_percent = len(site_data[0][1][i][1][j][1]) / summary_data[0][-2]
                    find_softbin = True
            if not find_softbin:
                temp_swbin_percent = 0
            temp_total_count += temp_swbin_percent
            temp_list.append([temp_swbin_percent, WHITE])
            if i == len(site_data[0][1]) - 1:
                temp_list.append([temp_total_count, 'FFA500'])
        site_swbin_percent.append(temp_list)

    for i in range(len(site_swbin_percent) - 1):
        min_value = site_swbin_percent[i][0][0]
        max_value = site_swbin_percent[i][0][0]
        for m in range(1, len(site_swbin_percent[i]) - 1):
            if min_value > site_swbin_percent[i][m][0]:
                min_value = site_swbin_percent[i][m][0]
            if max_value < site_swbin_percent[i][m][0]:
                max_value = site_swbin_percent[i][m][0]
        min_index = []
        max_index = []
        for j in range(len(site_swbin_percent[i]) - 1):
            if site_swbin_percent[i][j][0] == min_value:
                min_index.append(j)
            if site_swbin_percent[i][j][0] == max_value:
                max_index.append(j)
        if min_value == 0 and len(min_index) == 1:
            site_swbin_percent[i][min_index[0]][1] = GREEN
            for y in range(len(max_index)):
                site_swbin_percent[i][max_index[y]][1] = RED
        elif min_value == 0 and max_value > 0:
            for y in range(len(max_index)):
                site_swbin_percent[i][max_index[y]][1] = RED
        elif min_value > 0:
            for x in range(len(min_index)):
                site_swbin_percent[i][min_index[x]][1] = GREEN
            for y in range(len(max_index)):
                site_swbin_percent[i][max_index[y]][1] = RED

    for x in range(len(bin_list)):
        sitesoftbin_sheet.cell(row=irow, column=1).value = 'SWBin' + str(bin_list[x])
        if x <= 1:
            sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor='ADD8E6')
        elif 2 <= x <= 9:
            sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor='00FF7F')
        elif 10 <= x <= 22:
            sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor='EEE8AA')
        elif 23 <= x <= 32:
            sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor='FFA500')
        elif 33 <= x <= 36:
            sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor='CD853F')
        else:
            sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor='FF6347')
        for y in range(len(site_swbin_percent[x])):
            if y < len(site_swbin_percent[x]) - 1:
                if site_swbin_percent[x][y][0] > 0:
                    sitesoftbin_sheet.cell(row=irow, column=2 + y).value = '{:.2%}'.format(site_swbin_percent[x][y][0])
                sitesoftbin_sheet.cell(row=irow, column=2 + y).fill = PatternFill(fill_type='solid',
                                                                                  fgColor=site_swbin_percent[x][y][1])
            else:
                sitesoftbin_sheet.cell(row=irow, column=3 + y).value = '{:.2%}'.format(site_swbin_percent[x][y][0])
                sitesoftbin_sheet.cell(row=irow, column=3 + y).fill = PatternFill(fill_type='solid',
                                                                                  fgColor=site_swbin_percent[x][y][1])
        irow += 1

    for row in sitesoftbin_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1:
                cell.font = Font(bold=True)
                cell.alignment = alignment

    for sheet_name in wb.sheetnames:
        if sheet_name == 'Sheet':
            del wb[sheet_name]
        else:
            Common.set_column_width(wb[sheet_name])

    wb.save(test_file_name)


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

    hardbin_data = []
    softbin_data = []
    site_data = []
    for file in file_list:
        # parse file
        site_data.append(parse_file(file, 1))
        softbin_data.append(parse_file(file, 2))
        hardbin_data.append(parse_file(file, 3))

    for data in softbin_data:
        Common.sort_data(data[1])

    # save data
    save_data(analysis_folder, site_data, softbin_data, hardbin_data)


if __name__ == '__main__':
    main()
