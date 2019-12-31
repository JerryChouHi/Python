# encoding:utf-8
# @Time     : 2019/12/2
# @Author   : Jerry Chou
# @File     :
# @Function : 所有FT分析

from csv import reader
from os.path import basename, dirname, abspath, join, isdir
from os import getcwd, listdir
from datetime import datetime
from sys import argv, path
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
from openpyxl.styles.colors import YELLOW, GREEN, BLACK, WHITE, RED
from progressbar import *

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
    search_chipno = Common.search_string(data, 'ChipNo')
    if not search_chipno:
        exit()
    else:
        chipno_row_num = search_chipno[0]
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
    chip_count = first_register_row_num - chipno_row_num - row_offset
    return file_name, group_index, chip_count


def save_data(analysis_folder, site_data, softbin_data, project_id):
    """
    写数据
    :param analysis_folder: 保存分析文件夹路径
    :param site_data: site数据
    :return: 
    """
    date = datetime.now().strftime("%Y%m%d%H%M")
    test_file_name = analysis_folder + '/Total_Analysis_' + date + '.xlsx'
    wb = Workbook()

    hwbin_to_swbin_list = [
        [
            [1, [1, 2]],
            [2, [41, 42, 43, 44, 45, 53, 54, 55]],
            [4, [23, 24, 25, 29, 30, 33, 34, 36, 39, 40, 70, 71, 72]],
            [5, [5, 6, 7, 8, 9, 12, 96, 97, 98, 99]],
            [6, [13, 14, 15, 35]],
            [8, [26, 27, 31, 32]]  # 专门分出来测试良率
        ],
        [
            [3, [1, 2, 3]],
            [1, [63, 64, 65, 89, 90, 94]],
            [2, [53, 54, 73, 74]],
            [4, [23, 24, 25, 26, 27, 31, 32, 36, 56, 57, 58, 75]],
            [5, [5, 6, 7, 8, 9, 12, 93, 96, 98, 99]],
            [6, [13, 14, 15, 46, 47, 48, 51, 60]],
            [8, [29, 30, 33, 34, 36, 39, 40]]
        ]
    ]
    if project_id == 0:
        ok_hwbin_count = 2
    elif project_id == 1:
        ok_hwbin_count = 3

    begin_fail_swbin = 0
    for i in range(ok_hwbin_count):
        begin_fail_swbin += len(hwbin_to_swbin_list[project_id][i][1])

    color_list = ['99FFFF', '33FF00', 'FFFFCC', 'FFFF33', 'FF9900', '9900CC', 'FF0000']
    swbin_list = []
    for i in range(len(hwbin_to_swbin_list[project_id])):
        for j in range(len(hwbin_to_swbin_list[project_id][i][1])):
            swbin_list.append([hwbin_to_swbin_list[project_id][i][1][j], color_list[i]])

    sitesoftbin_sheet = wb.create_sheet('Site-SWBin')
    sitesoftbin_sheet.freeze_panes = 'B2'
    irow = 1
    total_count = 0
    for i in range(len(site_data)):
        total_count += site_data[i][1][0][2]
    sitesoftbin_sheet.cell(row=irow, column=1).value = total_count
    for i in range(len(site_data[0][1][0][1])):
        sitesoftbin_sheet.cell(row=irow, column=2 + i).value = 'Site' + str(site_data[0][1][0][1][i][0])
        sitesoftbin_sheet.cell(row=irow, column=2 + i).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
    sitesoftbin_sheet.merge_cells(start_row=irow, end_row=irow, start_column=3 + len(site_data[0][1][0][1]),
                                  end_column=4 + len(site_data[0][1][0][1]))
    sitesoftbin_sheet.cell(row=irow, column=3 + len(site_data[0][1][0][1])).value = 'Summary'
    sitesoftbin_sheet.cell(row=irow, column=3 + len(site_data[0][1][0][1])).fill = PatternFill(fill_type='solid',
                                                                                               fgColor='FFA500')
    irow += 1

    lotno_site_swbin_count = []

    site_swbin_widgets = ['Site-SWBin: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',
                          FileTransferSpeed()]
    site_swbin_pbar = ProgressBar(widgets=site_swbin_widgets, maxval=len(site_data)).start()
    for i in range(len(site_data)):
        lotno_temp_list = [site_data[i][0]]
        for x in range(begin_fail_swbin):
            file_temp_list = [swbin_list[x][0]]
            site_count_list = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                               [11, 0], [12, 0], [13, 0], [14, 0], [15, 0]]
            for m in range(len(site_data[i][1])):
                for n in range(len(site_data[i][1][m][1])):
                    for j in range(len(site_data[i][1][m][1][n][1])):
                        if site_data[i][1][m][1][n][1][j][0] == str(swbin_list[x][0]):
                            site_count_list[n][1] += len(site_data[i][1][m][1][n][1][j][1])
                            break
            file_temp_list.append(site_count_list)
            lotno_temp_list.append(file_temp_list)
        for x in range(begin_fail_swbin, len(swbin_list)):
            file_temp_list = [swbin_list[x][0]]
            site_count_list = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                               [11, 0], [12, 0], [13, 0], [14, 0], [15, 0]]
            for n in range(len(site_data[i][1][-1][1])):
                for j in range(len(site_data[i][1][-1][1][n][1])):
                    if site_data[i][1][-1][1][n][1][j][0] == str(swbin_list[x][0]):
                        site_count_list[n][1] += len(site_data[i][1][-1][1][n][1][j][1])
                        break
            file_temp_list.append(site_count_list)
            lotno_temp_list.append(file_temp_list)
        lotno_site_swbin_count.append(lotno_temp_list)
        site_swbin_pbar.update(i + 1)
    site_swbin_pbar.finish()
    site_swbin_count = []
    actual_total_count = 0
    for x in range(len(swbin_list)):
        temp_total_count = 0
        temp_list = [0] * 16
        temp_swbin_count = []
        for i in range(len(temp_list)):
            for y in range(len(lotno_site_swbin_count)):
                temp_list[i] += lotno_site_swbin_count[y][x + 1][1][i][1]
                if y == len(lotno_site_swbin_count) - 1:
                    temp_swbin_count.append([temp_list[i], WHITE])
                    temp_total_count += temp_list[i]
                    actual_total_count += temp_list[i]
            if i == len(temp_list) - 1:
                temp_swbin_count.append([temp_total_count, 'FFA500'])
        site_swbin_count.append(temp_swbin_count)
    site_pass_total_list = [0] * 16
    for i in range(begin_fail_swbin):
        for j in range(len(site_swbin_count[i]) - 1):
            site_pass_total_list[j] += site_swbin_count[i][j][0]
    site_fail_total_list = [0] * 16
    for i in range(begin_fail_swbin, len(site_swbin_count)):
        min_value = site_swbin_count[i][0][0]
        max_value = site_swbin_count[i][0][0]
        for m in range(1, len(site_swbin_count[i]) - 1):
            if min_value > site_swbin_count[i][m][0]:
                min_value = site_swbin_count[i][m][0]
            if max_value < site_swbin_count[i][m][0]:
                max_value = site_swbin_count[i][m][0]
        min_index = []
        max_index = []
        for j in range(len(site_swbin_count[i]) - 1):
            site_fail_total_list[j] += site_swbin_count[i][j][0]
            if site_swbin_count[i][j][0] == min_value:
                min_index.append(j)
            if site_swbin_count[i][j][0] == max_value:
                max_index.append(j)
        if min_value == 0 and len(min_index) == 1:
            site_swbin_count[i][min_index[0]][1] = GREEN
            for y in range(len(max_index)):
                site_swbin_count[i][max_index[y]][1] = RED
        elif min_value == 0 and max_value > 0:
            for y in range(len(max_index)):
                site_swbin_count[i][max_index[y]][1] = RED
        elif min_value > 0:
            for x in range(len(min_index)):
                site_swbin_count[i][min_index[x]][1] = GREEN
            for y in range(len(max_index)):
                site_swbin_count[i][max_index[y]][1] = RED

    for x in range(len(swbin_list)):
        sitesoftbin_sheet.cell(row=irow, column=1).value = 'SWBin' + str(swbin_list[x][0])
        sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=swbin_list[x][1])
        for y in range(len(site_swbin_count[x])):
            if y < len(site_swbin_count[x]) - 1:
                if site_swbin_count[x][y][0] > 0:
                    sitesoftbin_sheet.cell(row=irow, column=2 + y).value = '{:.4%}'.format(
                        site_swbin_count[x][y][0] / total_count)
                sitesoftbin_sheet.cell(row=irow, column=2 + y).fill = PatternFill(fill_type='solid',
                                                                                  fgColor=site_swbin_count[x][y][1])
            else:
                sitesoftbin_sheet.cell(row=irow, column=3 + y).value = site_swbin_count[x][y][0]
                sitesoftbin_sheet.cell(row=irow, column=4 + y).value = '{:.4%}'.format(
                    site_swbin_count[x][y][0] / total_count)
                sitesoftbin_sheet.cell(row=irow, column=4 + y).fill = PatternFill(fill_type='solid',
                                                                                  fgColor=site_swbin_count[x][y][1])
        irow += 1
    irow += 1
    sitesoftbin_sheet.merge_cells(start_row=irow, end_row=irow + 1, start_column=1, end_column=1)
    sitesoftbin_sheet.cell(row=irow, column=1).value = 'FailPercent'
    sitesoftbin_sheet.cell(row=irow, column=1).font = Font(bold=True)
    sitesoftbin_sheet.cell(row=irow, column=1).alignment = alignment
    sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=RED)
    for i in range(len(site_fail_total_list)):
        sitesoftbin_sheet.cell(row=irow, column=2 + i).value = site_fail_total_list[i]
        sitesoftbin_sheet.cell(row=irow + 1, column=2 + i).value = '{:.4%}'.format(
            site_fail_total_list[i] / total_count)
        sitesoftbin_sheet.cell(row=irow + 1, column=2 + i).fill = PatternFill(fill_type='solid', fgColor=RED)
    sitesoftbin_sheet.cell(row=irow, column=3 + len(site_fail_total_list)).value = sum(site_fail_total_list)
    sitesoftbin_sheet.cell(row=irow, column=3 + len(site_fail_total_list)).fill = PatternFill(fill_type='solid',
                                                                                              fgColor=RED)
    sitesoftbin_sheet.cell(row=irow + 1, column=3 + len(site_fail_total_list)).value = '{:.4%}'.format(
        sum(site_fail_total_list) / total_count)
    sitesoftbin_sheet.cell(row=irow + 1, column=3 + len(site_fail_total_list)).fill = PatternFill(fill_type='solid',
                                                                                                  fgColor=RED)
    irow += 2
    sitesoftbin_sheet.merge_cells(start_row=irow, end_row=irow + 1, start_column=1, end_column=1)
    sitesoftbin_sheet.cell(row=irow, column=1).value = 'PassPercent'
    sitesoftbin_sheet.cell(row=irow, column=1).font = Font(bold=True)
    sitesoftbin_sheet.cell(row=irow, column=1).alignment = alignment
    sitesoftbin_sheet.cell(row=irow, column=1).fill = PatternFill(fill_type='solid', fgColor=GREEN)
    for i in range(len(site_pass_total_list)):
        sitesoftbin_sheet.cell(row=irow, column=2 + i).value = site_pass_total_list[i]
        sitesoftbin_sheet.cell(row=irow + 1, column=2 + i).value = '{:.4%}'.format(
            site_pass_total_list[i] / total_count)
        sitesoftbin_sheet.cell(row=irow + 1, column=2 + i).fill = PatternFill(fill_type='solid', fgColor=GREEN)
    sitesoftbin_sheet.cell(row=irow, column=3 + len(site_pass_total_list)).value = sum(site_pass_total_list)
    sitesoftbin_sheet.cell(row=irow, column=3 + len(site_pass_total_list)).fill = PatternFill(fill_type='solid',
                                                                                              fgColor=GREEN)
    sitesoftbin_sheet.cell(row=irow + 1, column=3 + len(site_pass_total_list)).value = '{:.4%}'.format(
        sum(site_pass_total_list) / total_count)
    sitesoftbin_sheet.cell(row=irow + 1, column=3 + len(site_pass_total_list)).fill = PatternFill(fill_type='solid',
                                                                                                  fgColor=GREEN)

    for row in sitesoftbin_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1:
                cell.font = Font(bold=True)
                cell.alignment = alignment

    softbinlotno_sheet = wb.create_sheet('LotNo-SWBin')
    softbinlotno_sheet.freeze_panes = 'C2'
    softbinlotno_sheet.cell(row=1, column=1).value = len(softbin_data)
    softbinlotno_sheet.cell(row=1, column=2).value = total_count
    for i in range(len(softbin_data)):
        softbinlotno_sheet.cell(row=2 + i, column=1).value = softbin_data[i][2]
        softbinlotno_sheet.cell(row=2 + i, column=2).value = softbin_data[i][0]
        softbinlotno_sheet.cell(row=2 + i, column=2).fill = PatternFill(fill_type='solid', fgColor=YELLOW)

    lotno_swbin_count = []

    lotno_swbin_widgets = ['LotNo_SWBin: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',
                           FileTransferSpeed()]
    lotno_swbin_pbar = ProgressBar(widgets=lotno_swbin_widgets, maxval=len(softbin_data)).start()
    for i in range(len(softbin_data)):
        lotno_temp_list = []
        for x in range(begin_fail_swbin):
            file_temp_list = [swbin_list[x][0], 0]
            for m in range(len(softbin_data[i][1])):
                for n in range(len(softbin_data[i][1][m][1])):
                    if softbin_data[i][1][m][1][n][0] == swbin_list[x][0]:
                        file_temp_list[1] += len(softbin_data[i][1][m][1][n][1])
                        break
            lotno_temp_list.append(file_temp_list)
        for x in range(begin_fail_swbin, len(swbin_list)):
            file_temp_list = [swbin_list[x][0], 0]
            for n in range(len(softbin_data[i][1][-1][1])):
                if softbin_data[i][1][-1][1][n][0] == swbin_list[x][0]:
                    file_temp_list[1] += len(softbin_data[i][1][-1][1][n][1])
                    break
            lotno_temp_list.append(file_temp_list)
        lotno_swbin_count.append(lotno_temp_list)
        lotno_swbin_pbar.update(i + 1)
    lotno_swbin_pbar.finish()
    for x in range(len(swbin_list)):
        softbinlotno_sheet.merge_cells(start_row=1, end_row=1, start_column=3 + 2 * x, end_column=4 + 2 * x)
        softbinlotno_sheet.cell(row=1, column=3 + 2 * x).value = 'SWBin' + str(swbin_list[x][0])
        softbinlotno_sheet.cell(row=1, column=3 + 2 * x).fill = PatternFill(fill_type='solid', fgColor=swbin_list[x][1])
        for i in range(len(lotno_swbin_count)):
            softbinlotno_sheet.cell(row=2 + i, column=3 + 2 * x).value = lotno_swbin_count[i][x][1]
            softbinlotno_sheet.cell(row=2 + i, column=4 + 2 * x).value = '{:.2%}'.format(
                lotno_swbin_count[i][x][1] / softbin_data[i][1][0][2])
            softbinlotno_sheet.cell(row=2 + i, column=4 + 2 * x).fill = PatternFill(fill_type='solid',
                                                                                    fgColor=swbin_list[x][1])

    for row in softbinlotno_sheet.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1 or cell.column in (1, 2):
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
    if argv.count('-s') == 0:
        print("Error：Sourcefile folder path 为必填项，格式：“-s D:\sourcefile”")
        exit()
    else:
        sourcefile_folder = argv[argv.index('-s') + 1]
        for i in range(argv.index('-s') + 2, len(argv)):
            if not argv[i].startswith('-'):
                sourcefile_folder += (' ' + argv[i])
            else:
                break

    # 项目 0:F28,1:JX828
    if argv.count('-p') != 0:
        project_id = int(argv[argv.index('-p') + 1])
    else:
        project_id = 0  # 默认F28项目

    names = listdir(sourcefile_folder)
    date_folder = []
    for name in names:
        if name != 'Analysis' and isdir(join(sourcefile_folder, name)):
            date_folder.append(join(sourcefile_folder, name))
    lotno_folder = []
    for folder in date_folder:
        names = listdir(folder)
        for name in names:
            if isdir(join(folder, name)):
                lotno_folder.append(join(folder, name))
    file_list = []
    for folder in lotno_folder:
        file_list.append(Common.get_filelist(folder, '.csv'))
        if not file_list:
            exit()

    # Analysis folder path
    if argv.count('-a') == 0:
        analysis_folder = sourcefile_folder + '\Analysis'
    else:
        analysis_folder = argv[argv.index('-a') + 1]

    Common.mkdir(analysis_folder)

    site_data = []
    softbin_data = []

    parse_file_widgets = ['ParseFile: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',
                          FileTransferSpeed()]
    parse_file_pbar = ProgressBar(widgets=parse_file_widgets, maxval=len(file_list)).start()
    for i in range(len(file_list)):
        temp_site_data = []
        temp_softbin_data = []
        for file in file_list[i]:
            # parse file
            temp_site_data.append(parse_file(file, 1))
            temp_softbin_data.append(parse_file(file, 2))
        date = basename(dirname(dirname(file_list[i][0])))
        lotno = basename(lotno_folder[i])
        site_data.append([lotno, temp_site_data, date])
        softbin_data.append([lotno, temp_softbin_data, date])
        parse_file_pbar.update(i + 1)
    parse_file_pbar.finish()

    # save data
    save_data(analysis_folder, site_data, softbin_data, project_id)


if __name__ == '__main__':
    main()
