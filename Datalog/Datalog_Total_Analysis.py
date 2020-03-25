# encoding:utf-8
# @Time     : 2019/12/2
# @Author   : Jerry Chou
# @File     :
# @Function : analysis all data

from csv import reader, field_size_limit
from os.path import basename, dirname, exists, join, isdir
from os import listdir, makedirs, getcwd
from datetime import datetime
from sys import argv, exit, maxsize
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
from openpyxl.styles.colors import YELLOW, GREEN, BLACK, WHITE, RED
from openpyxl.utils import get_column_letter
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QComboBox, QFileDialog, QProgressBar, \
    QErrorMessage, QRadioButton
from PyQt5.QtCore import QThread, pyqtSignal, QRect
from PyQt5.QtGui import QIcon, QBrush, QPixmap, QPalette


def find_item(item_list, value):
    """
    find value in item list
    """
    return [i for i, v in enumerate(item_list) if v == value]


def search_string(data, target):
    """
    find out if target exists in data
    """
    for i in range(len(data)):
        try:
            col_num = data[i].index(target)
            row_num = i
            return row_num, col_num
        except:
            pass
    print("Can't find " + target + " !")
    return False


def set_column_width(sheet):
    """
    set column width
    """
    # get the maximum width of each column
    col_width = [0.5] * sheet.max_column
    for row in range(sheet.max_row):
        for col in range(sheet.max_column):
            value = sheet.cell(row=row + 1, column=col + 1).value
            if value:
                width = len(str(value))
                if width > col_width[col]:
                    col_width[col] = width
    # set column width
    for i in range(len(col_width)):
        col_lettert = get_column_letter(i + 1)
        if col_width[i] > 100:
            # set to 100 if col_width greater than 100
            sheet.column_dimensions[col_lettert].width = 100
        else:
            sheet.column_dimensions[col_lettert].width = col_width[i] + 4


def get_filelist(folder, postfix=None):
    """
    find a list of files with a postfix
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
        print("Error：Not a folder!")
        return False


def mkdir(path):
    """
    create a folder
    """
    path = path.strip()
    path = path.rstrip("\\")
    is_exists = exists(path)
    if not is_exists:
        makedirs(path)
        return True
    else:
        return False


alignment = Alignment(horizontal='center', vertical='center')
thin = Side(border_style='thin', color=BLACK)
border = Border(top=thin, left=thin, right=thin, bottom=thin)

row_offset = 5
# default project
project = 'F28'
lotCount = 0
now_time = datetime.now().strftime("%Y%m%d%H%M%S")

hwbin_to_swbin = {
    'F28': {
        1: {'SWBin': (1, 2), 'isPassBin': True},
        2: {'SWBin': (41, 42, 43, 44, 45, 53, 54, 55), 'isPassBin': True},
        4: {'SWBin': (23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 36, 39, 40, 70, 71, 72), 'isPassBin': False},
        5: {'SWBin': (5, 6, 7, 8, 9, 12, 96, 97, 98, 99), 'isPassBin': False},
        6: {'SWBin': (13, 14, 15, 35), 'isPassBin': False}
    },
    'JX828': {
        3: {'SWBin': (1, 2, 3), 'isPassBin': True},
        1: {'SWBin': (63, 64, 65, 89, 90, 94), 'isPassBin': True},
        2: {'SWBin': (53, 54, 73, 74), 'isPassBin': True},
        4: {'SWBin': (23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 36, 39, 40, 56, 57, 58, 75), 'isPassBin': False},
        5: {'SWBin': (5, 6, 7, 8, 9, 12, 93, 96, 98, 99), 'isPassBin': False},
        6: {'SWBin': (13, 14, 15, 35, 46, 47, 48, 51, 60), 'isPassBin': False}
    },
    'JX825': {
        3: {'SWBin': (2, 255), 'isPassBin': True},
        4: {'SWBin': (23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 36, 39, 40, 63, 64, 65), 'isPassBin': False},
        5: {'SWBin': (5, 6, 7, 8, 9, 12, 89), 'isPassBin': False},
        6: {'SWBin': (13, 14, 15, 35, 46, 48, 53, 54, 60), 'isPassBin': False},
        8: {'SWBin': (94, 96, 97, 98, 99), 'isPassBin': False}
    }
}


def parse_file(file, group_by_id):
    """
    get basic information and group data
    """
    parse_result = {}
    data = []
    # get file data
    with open(file, encoding='unicode_escape') as f:
        csv_reader = reader((line.replace('\0', '') for line in f))
        for row in csv_reader:
            data.append(row)

    # get row of ChipNo
    search_chipno = search_string(data, 'ChipNo')
    if not search_chipno:
        exit()
    else:
        chipno_row_num = search_chipno[0]

    # get row of first register
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

    group_index = {}
    for i in format_group_list:
        temp = []
        data_list = find_item(group_list, i)
        if group_by_id == 1:
            temp_list = []
            for j in data_list:
                # get the corresponding SW_BIN of Site
                temp_list.append(data[chipno_row_num + row_offset + j][2])
            # remove duplicate value
            format_temp_list = list(set(temp_list))
            temp_index = {}
            for m in format_temp_list:
                # find m in temp_list
                temp_data_list = find_item(temp_list, m)
                temp_index[m] = temp_data_list
            temp.append(temp_index)
        else:
            temp.append(data_list)
        group_index[i] = temp
    # calculate chip count
    chip_count = first_register_row_num - chipno_row_num - row_offset
    parse_result['group index'] = group_index
    parse_result['chip count'] = chip_count
    return parse_result


def get_lotno(file):
    """
    get lotno
    """
    data = []
    # get file data
    with open(file, encoding='unicode_escape') as f:
        csv_reader = reader((line.replace('\0', '') for line in f))
        for row in csv_reader:
            data.append(row)
    # get lotno
    lotno = data[5][1]
    return lotno


def save_data(analysis_file, parse_data):
    """
    save data to file
    """
    wb = Workbook()

    ok_hwbin_count = 0
    begin_fail_swbin = 0
    for hw_bin_key in hwbin_to_swbin[project].keys():
        if hwbin_to_swbin[project][hw_bin_key]['isPassBin']:
            ok_hwbin_count += 1
            begin_fail_swbin += len(hwbin_to_swbin[project][hw_bin_key]['SWBin'])

    color_list = ['99FFFF', '33FF00', 'FFFFCC', 'FFFF33', 'FF9900', 'FF0099', 'FF0000']
    swbin_list = []
    key_index = 0
    for hwbin_key in hwbin_to_swbin[project].keys():
        for swbin in hwbin_to_swbin[project][hwbin_key]['SWBin']:
            swbin_list.append([swbin, color_list[key_index]])
        key_index += 1

    sitesoftbin_sheet = wb.create_sheet('Site-SWBin')
    sitesoftbin_sheet.freeze_panes = 'B2'
    irow = 1
    total_count = 0
    for i in range(len(parse_data)):
        total_count += parse_data[i]['site data'][0]['chip count']
    sitesoftbin_sheet.cell(row=irow, column=1).value = total_count
    for i in range(16):
        sitesoftbin_sheet.cell(row=irow, column=2 + i).value = 'Site' + str(i)
        sitesoftbin_sheet.cell(row=irow, column=2 + i).fill = PatternFill(fill_type='solid', fgColor=YELLOW)
    sitesoftbin_sheet.merge_cells(start_row=irow, end_row=irow, start_column=19, end_column=20)
    sitesoftbin_sheet.cell(row=irow, column=19).value = 'Summary'
    sitesoftbin_sheet.cell(row=irow, column=19).fill = PatternFill(fill_type='solid', fgColor='FFA500')
    irow += 1

    lotno_site_swbin_count = []
    for i in range(len(parse_data)):
        lotno_temp_list = [parse_data[i]['lotno']]
        for x in range(len(swbin_list)):
            swbin = str(swbin_list[x][0])
            file_temp_list = [swbin_list[x][0]]
            site_count_list = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],
                               [11, 0], [12, 0], [13, 0], [14, 0], [15, 0]]
            for site in range(16):
                if x < begin_fail_swbin:
                    for m in range(len(parse_data[i]['site data'])):
                        if (site in parse_data[i]['site data'][m]['group index'].keys()) and (
                                    swbin in parse_data[i]['site data'][m]['group index'][site][0].keys()):
                            site_count_list[site][1] += len(
                                parse_data[i]['site data'][m]['group index'][site][0][swbin])
                else:
                    if (site in parse_data[i]['site data'][-1]['group index'].keys()) and (
                                swbin in parse_data[i]['site data'][-1]['group index'][site][0].keys()):
                        site_count_list[site][1] += len(parse_data[i]['site data'][-1]['group index'][site][0][swbin])
            file_temp_list.append(site_count_list)
            lotno_temp_list.append(file_temp_list)
        lotno_site_swbin_count.append(lotno_temp_list)
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
    # add the number of fail swbin by all site
    # fill color of max value in fail swbin is green(all values are 0 do not fill green)
    # fill color of min value in fail swbin is red(multiple values of 0 do not fill red)
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
    softbinlotno_sheet.freeze_panes = 'D2'
    softbinlotno_sheet.cell(row=1, column=1).value = len(parse_data)
    softbinlotno_sheet.cell(row=1, column=2).value = total_count
    softbinlotno_sheet.cell(row=1, column=3).value = 'PassPercent'
    for i in range(len(parse_data)):
        softbinlotno_sheet.cell(row=2 + i, column=1).value = parse_data[i]['date']
        softbinlotno_sheet.cell(row=2 + i, column=2).value = parse_data[i]['lotno']
        softbinlotno_sheet.cell(row=2 + i, column=2).fill = PatternFill(fill_type='solid', fgColor=YELLOW)

    lotno_swbin_count = []

    for i in range(len(parse_data)):
        lotno_temp_list = []
        for x in range(len(swbin_list)):
            swbin = swbin_list[x][0]
            file_temp_list = [swbin, 0]
            if x < begin_fail_swbin:
                for m in range(len(parse_data[i]['swbin data'])):
                    if swbin in parse_data[i]['swbin data'][m]['group index'].keys():
                        file_temp_list[1] += len(parse_data[i]['swbin data'][m]['group index'][swbin][0])
            else:
                if swbin in parse_data[i]['swbin data'][-1]['group index'].keys():
                    file_temp_list[1] += len(parse_data[i]['swbin data'][-1]['group index'][swbin][0])
            lotno_temp_list.append(file_temp_list)
        lotno_swbin_count.append(lotno_temp_list)
    for x in range(len(swbin_list)):
        softbinlotno_sheet.merge_cells(start_row=1, end_row=1, start_column=4 + 2 * x, end_column=5 + 2 * x)
        softbinlotno_sheet.cell(row=1, column=4 + 2 * x).value = 'SWBin' + str(swbin_list[x][0])
        softbinlotno_sheet.cell(row=1, column=4 + 2 * x).fill = PatternFill(fill_type='solid', fgColor=swbin_list[x][1])
        for i in range(len(lotno_swbin_count)):
            pass_count = 0
            for j in range(begin_fail_swbin):
                pass_count += lotno_swbin_count[i][j][1]
            softbinlotno_sheet.cell(row=2 + i, column=3).value = '{:.2%}'.format(
                pass_count / parse_data[i]['swbin data'][0]['chip count'])
            if pass_count >= parse_data[i]['swbin data'][0]['chip count']:
                softbinlotno_sheet.cell(row=2 + i, column=3).fill = PatternFill(fill_type='solid', fgColor=RED)
            softbinlotno_sheet.cell(row=2 + i, column=4 + 2 * x).value = lotno_swbin_count[i][x][1]
            softbinlotno_sheet.cell(row=2 + i, column=5 + 2 * x).value = '{:.2%}'.format(
                lotno_swbin_count[i][x][1] / parse_data[i]['swbin data'][0]['chip count'])
            softbinlotno_sheet.cell(row=2 + i, column=5 + 2 * x).fill = PatternFill(fill_type='solid',
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
            set_column_width(wb[sheet_name])

    wb.save(analysis_file)


class Runthread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self, open_path, choose_radio):
        super(Runthread, self).__init__()
        self.open_path = open_path
        self.choose_radio = choose_radio
        self.count = 0

    def __del__(self):
        self.wait()

    def run(self):
        if self.choose_radio=='ProjectFolder':
            handler_names = listdir(self.open_path)
            handler_folders = []
            for handler_name in handler_names:
                if isdir(join(self.open_path, handler_name)):
                    handler_folders.append(join(self.open_path, handler_name))

            for handler_folder in handler_folders:
                date_folders = []
                date_names = listdir(handler_folder)
                for date_name in date_names:
                    if date_name != 'Analysis' and isdir(join(handler_folder, date_name)):
                        date_folders.append(join(handler_folder, date_name))

                lotno_folders = []
                for date_folder in date_folders:
                    lot_names = listdir(date_folder)
                    for lot_name in lot_names:
                        if isdir(join(date_folder, lot_name)):
                            lotno_folders.append(join(date_folder, lot_name))
                file_list = []
                for lot_folder in lotno_folders:
                    # get CSV file under the folder
                    file_list.append(get_filelist(lot_folder, '.csv'))
                    if not file_list:
                        exit()

                # analysis folder path
                if argv.count('-a') == 0:
                    analysis_folder = handler_folder + '\Analysis'
                else:
                    analysis_folder = argv[argv.index('-a') + 1]

                mkdir(analysis_folder)

                parse_data = []

                for i in range(len(file_list)):
                    lotno_data = {}
                    temp_site_data = []
                    temp_softbin_data = []
                    for file in file_list[i]:
                        # parse file
                        temp_site_data.append(parse_file(file, 1))
                        temp_softbin_data.append(parse_file(file, 2))
                    # get Date
                    date = basename(dirname(dirname(file_list[i][0])))
                    lotno_data['site data'] = temp_site_data
                    lotno_data['swbin data'] = temp_softbin_data
                    lotno_data['date'] = date
                    lotno_data['lotno'] = get_lotno(file_list[i][0])
                    parse_data.append(lotno_data)
                    self.count += 1
                    self._signal.emit(str(self.count * 100 // lotCount))
                handler = basename(handler_folder)
                analysis_file = join(analysis_folder, handler + '_Total_Analysis' + now_time + '.xlsx')
                # save data
                save_data(analysis_file, parse_data)
        else:
            date_folders = []
            date_names = listdir(self.open_path)
            for date_name in date_names:
                if date_name != 'Analysis' and isdir(join(self.open_path, date_name)):
                    date_folders.append(join(self.open_path, date_name))

            lotno_folders = []
            for date_folder in date_folders:
                lot_names = listdir(date_folder)
                for lot_name in lot_names:
                    if isdir(join(date_folder, lot_name)):
                        lotno_folders.append(join(date_folder, lot_name))
            file_list = []
            for lot_folder in lotno_folders:
                # get CSV file under the folder
                file_list.append(get_filelist(lot_folder, '.csv'))
                if not file_list:
                    exit()

            # analysis folder path
            if argv.count('-a') == 0:
                analysis_folder = self.open_path + '\Analysis'
            else:
                analysis_folder = argv[argv.index('-a') + 1]

            mkdir(analysis_folder)

            parse_data = []

            for i in range(len(file_list)):
                lotno_data = {}
                temp_site_data = []
                temp_softbin_data = []
                for file in file_list[i]:
                    # parse file
                    temp_site_data.append(parse_file(file, 1))
                    temp_softbin_data.append(parse_file(file, 2))
                # get Date
                date = basename(dirname(dirname(file_list[i][0])))
                lotno_data['site data'] = temp_site_data
                lotno_data['swbin data'] = temp_softbin_data
                lotno_data['date'] = date
                lotno_data['lotno'] = get_lotno(file_list[i][0])
                parse_data.append(lotno_data)
                self.count += 1
                self._signal.emit(str(self.count * 100 // lotCount))
            handler = basename(self.open_path)
            analysis_file = join(analysis_folder, handler + '_Total_Analysis' + now_time + '.xlsx')
            # save data
            save_data(analysis_file, parse_data)
        self._signal.emit(str(100))


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cwd = getcwd()
        self.qe = QErrorMessage(self)
        self.pale = QPalette()
        self.open_edit = QLineEdit(self)
        self.open_button = QPushButton('Open', self)
        self.analysis_button = QPushButton('Analysis', self)
        self.progressBar = QProgressBar(self)
        self.combobox = QComboBox(self)
        self.ProjectFolder_radioButton = QRadioButton('ProjectFolder', self)
        self.HandlerFolder_radioButton = QRadioButton('HandlerFolder', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Datalog Total Analysis')
        self.setWindowIcon(QIcon('./icos/favicon.ico'))
        self.pale.setBrush(self.backgroundRole(), QBrush(QPixmap('./images/kobe3.jpg')))
        self.setPalette(self.pale)
        self.setMaximumSize(800, 600)
        self.setMinimumSize(800, 600)

        self.ProjectFolder_radioButton.setGeometry(QRect(50, 20, 100, 30))
        self.ProjectFolder_radioButton.setChecked(True)
        self.ProjectFolder_radioButton.toggled.connect(self.choose)
        self.HandlerFolder_radioButton.setGeometry(QRect(170, 20, 100, 30))
        self.HandlerFolder_radioButton.toggled.connect(self.choose)

        self.open_edit.setGeometry(QRect(50, 80, 500, 50))
        self.open_edit.setReadOnly(True)

        self.open_button.setGeometry(QRect(580, 80, 170, 50))
        # click button call openfolder
        self.open_button.clicked.connect(self.open)

        self.combobox.setGeometry(QRect(50, 180, 200, 50))
        self.combobox.insertItem(0, self.tr('F28'))
        self.combobox.insertItem(1, self.tr('JX828'))
        self.combobox.insertItem(2, self.tr('JX825'))

        self.analysis_button.setGeometry(QRect(280, 180, 170, 50))
        self.analysis_button.clicked.connect(self.analysis)

        self.progressBar.setGeometry(QRect(50, 280, 700, 30))
        self.progressBar.setValue(0)

        self.show()

    def choose(self):
        if self.HandlerFolder_radioButton.isChecked():
            self.ProjectFolder_radioButton.setChecked(False)
        else:
            self.HandlerFolder_radioButton.setChecked(False)

    def open(self):
        dir_choose = QFileDialog.getExistingDirectory(self, 'Select directory', self.cwd)
        if not dir_choose:
            return
        self.open_edit.setText(dir_choose)
        global lotCount
        lotCount = 0
        if self.ProjectFolder_radioButton.isChecked():
            handler_names = listdir(self.open_edit.text())
            handler_folders = []
            for handler_name in handler_names:
                if isdir(join(self.open_edit.text(), handler_name)):
                    handler_folders.append(join(self.open_edit.text(), handler_name))
            if not handler_folders:
                self.qe.showMessage('Path is incorrect,please check!')
                return
            for handler_folder in handler_folders:
                date_folders = []
                date_names = listdir(handler_folder)
                for date_name in date_names:
                    if date_name != 'Analysis' and isdir(join(handler_folder, date_name)):
                        date_folders.append(join(handler_folder, date_name))
                if not date_folders:
                    self.qe.showMessage('Path is incorrect,please check!')
                    return
                lotno_folders = []
                for date_folder in date_folders:
                    lot_names = listdir(date_folder)
                    for lot_name in lot_names:
                        if isdir(join(date_folder, lot_name)):
                            lotno_folders.append(join(date_folder, lot_name))
                if not lotno_folders:
                    self.qe.showMessage('Path is incorrect,please check!')
                    return
                lotCount += len(lotno_folders)
        else:
            date_folders = []
            date_names = listdir(self.open_edit.text())
            for date_name in date_names:
                if date_name != 'Analysis' and isdir(join(self.open_edit.text(), date_name)):
                    date_folders.append(join(self.open_edit.text(), date_name))
            if not date_folders:
                self.qe.showMessage('Path is incorrect,please check!')
                return
            lotno_folders = []
            for date_folder in date_folders:
                lot_names = listdir(date_folder)
                for lot_name in lot_names:
                    if isdir(join(date_folder, lot_name)):
                        lotno_folders.append(join(date_folder, lot_name))
            if not lotno_folders:
                self.qe.showMessage('Path is incorrect,please check!')
                return
            lotCount += len(lotno_folders)


    def call_backlog(self, msg):
        self.progressBar.setValue(int(msg))  # pass the thread's parameters to progressBar
        if msg == '100':
            # del self.thread
            self.analysis_button.setEnabled(True)

    def analysis(self):
        if not self.open_edit.text():
            self.qe.showMessage('Path cannot be empty!')
            return
        else:
            if lotCount == 0:
                return
            self.progressBar.setValue(0)
            global project
            project = self.combobox.currentText()
            if self.ProjectFolder_radioButton.isChecked():
                choose_radio = self.ProjectFolder_radioButton.text()
            else:
                choose_radio = self.HandlerFolder_radioButton.text()
            # create thread
            self.analysis_button.setEnabled(False)
            self.thread = Runthread(self.open_edit.text(), choose_radio)
            # connect signal
            self.thread._signal.connect(self.call_backlog)
            self.thread.start()


if __name__ == '__main__':
    # _csv.Error:field larger than field limit(131072)
    maxInt = maxsize
    while True:
        try:
            field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)
    app = QApplication(argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    exit(app.exec_())
