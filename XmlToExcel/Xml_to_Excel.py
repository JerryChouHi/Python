# encoding:utf-8
# @Time     : 2019/11/1 10:21
# @Author   : Jerry Chou
# @File     : Xml_to_Excel.py
# @Function :

from sys import argv, path
from os.path import abspath,join
from os import getcwd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
from openpyxl.styles.colors import RED, YELLOW, GREEN, BLACK
from openpyxl.utils import quote_sheetname
from openpyxl.worksheet.datavalidation import DataValidation
from xml.dom.minidom import parse

path.append(abspath(join(getcwd(), '..')))
import Common

alignment = Alignment(horizontal='center', vertical='center')
thin = Side(border_style='thin', color=BLACK)
border = Border(top=thin, left=thin, right=thin, bottom=thin)


def read_project(project_folder):
    socketmap_path = path.join(project_folder, "Project.xml")
    dom = parse(socketmap_path)
    root = dom.documentElement
    socketmap = root.getElementsByTagName('SocketMap')
    datalog = root.getElementsByTagName('Datalog')
    projectsetup = root.getElementsByTagName('ProjectSetup')
    project_data = []
    for item in socketmap:
        project_data.append(Common.get_tree(item))
    for item in datalog:
        project_data.append(Common.get_tree(item))
    for item in projectsetup:
        project_data.append(Common.get_tree(item))
    return project_data


def read_socketmap(project_folder):
    socketmap_path = path.join(project_folder, "XML\\SocketMap.xml")
    dom = parse(socketmap_path)
    root = dom.documentElement
    itemlist = root.getElementsByTagName('SignalRef')
    socketmap_data = []
    for item in itemlist:
        socketmap_data.append(Common.get_tree(item))
    return socketmap_data


def read_signals(project_folder):
    signals_path = path.join(project_folder, "XML\\Signals.xml")
    dom = parse(signals_path)
    root = dom.documentElement
    itemlist = root.getElementsByTagName('Signal')
    signals_data = []
    for item in itemlist:
        signals_data.append(Common.get_tree(item))
    return signals_data


def read_limit(project_folder):
    limit_path = path.join(project_folder, "XML\\Limit.xml")
    dom = parse(limit_path)
    root = dom.documentElement
    itemlist = root.getElementsByTagName('Limit')
    limit_data = []
    for item in itemlist:
        limit_data.append(Common.get_tree(item))
    return limit_data


def read_signalgroups(project_folder):
    signalgroups_path = path.join(project_folder, "XML\\SignalGroups.xml")
    dom = parse(signalgroups_path)
    root = dom.documentElement
    itemlist = root.getElementsByTagName('Signalgroup')
    signalgroups_data = []
    for item in itemlist:
        signalgroups_data.append(Common.get_tree(item))
    return signalgroups_data


def read_bindefinition(project_folder):
    bindefinition_path = path.join(project_folder, "XML\\BinDefinition.xml")
    dom = parse(bindefinition_path)
    root = dom.documentElement
    itemlist = root.getElementsByTagName('BinGroup')
    bindefinition_data = []
    for item in itemlist:
        if item.getAttribute('name') == 'HardBins':
            bindefinition_data.append(Common.get_tree(item))
        elif item.getAttribute('name') == 'SoftBins':
            bindefinition_data.append(Common.get_tree(item))
    return bindefinition_data


def read_dcmeasure(project_folder):
    testblock_path = path.join(project_folder, "XML\\TestBlock.xml")
    dom = parse(testblock_path)
    root = dom.documentElement
    itemlist = root.getElementsByTagName('DCMeasure')
    dcmeasure_data = []
    for item in itemlist:
        dcmeasure_data.append(Common.get_tree(item))
    return dcmeasure_data


def read_tests(project_folder):
    testblock_path = path.join(project_folder, "XML\\TestBlock.xml")
    dom = parse(testblock_path)
    root = dom.documentElement
    itemlist = root.getElementsByTagName('Test')
    tests_data = []
    for item in itemlist:
        tests_data.append(Common.get_tree(item))
    return tests_data


def read_uservars(project_folder):
    uservars_path = path.join(project_folder, "XML\\UserVars.xml")
    dom = parse(uservars_path)
    root = dom.documentElement
    itemlist = root.getElementsByTagName('Variable')
    uservars_data = []
    for item in itemlist:
        uservars_data.append(Common.get_tree(item))
    return uservars_data


def read_levels(project_folder):
    levels_path = path.join(project_folder, "XML\\Levels.xml")
    dom = parse(levels_path)
    root = dom.documentElement
    itemlist = root.getElementsByTagName('Levels')
    levels_data = []
    for item in itemlist:
        levels_data.append(Common.get_tree(item))
    return levels_data


def write_excel(project_data, socketmap_data, signals_data, limit_data, signalgroups_data, bindefinition_data,
                dcmeasure_data, tests_data, uservars_data, levels_data):
    file_name = 'Project.xlsx'

    wb = Workbook()  # 创建文件对象

    dv_SignalType = DataValidation(type='list', formula1='"In,Out,InOut,Supply,Pseudo,System"', allow_blank=True)
    dv_Unit = DataValidation(type='list', formula1='"A,mA,uA,V,mV"', allow_blank=True)
    dv_HWBinPassFail = DataValidation(type='list', formula1='"Pass,Fail"', allow_blank=True)
    dv_MeasureModeType = DataValidation(type='list', formula1='"FVMI,FIMV,FVMV,FIMI"', allow_blank=True)
    dv_MeasureMethodType = DataValidation(type='list', formula1='"Parallel,Serial"', allow_blank=True)
    dv_VariableType = DataValidation(type='list',
                                     formula1='"Voltage,Current,Time,Frequency,Resistance,Capacitance,SingleValue"',
                                     allow_blank=True)
    dv_PatternExecModeType = DataValidation(type='list', formula1='"Burst,Individual"', allow_blank=True)
    dv_TestParamType = DataValidation(type='list',
                                      formula1='"SocketMap,PatternBurst,DCMeasure,Value_String,Value_Voltage,Value_Current,Value_Time,Value_Frequency,Value_Resistance,Value_Capacitance,Value_Single"',
                                      allow_blank=True)

    sigref_str = ''
    for i in range(len(signals_data)):
        if signals_data[i][1][0][1] in ('Supply,InOut'):
            sigref_str += (signals_data[i][0][1] + ',')
    for i in range(len(signalgroups_data)):
        if signalgroups_data[i][1][0][1] in ('Supply,InOut'):
            sigref_str += (signalgroups_data[i][0][1] + ',')
    sigref_str = sigref_str[:-1]
    dv_sigref = DataValidation(type='list', formula1='"' + sigref_str + '"', allow_blank=True)

    sheet_project = wb.create_sheet('Project')
    sheet_project.add_data_validation(dv_SignalType)
    sheet_project.freeze_panes = 'B1'
    irow = 1
    sheet_project.cell(row=irow, column=1).value = 'SocketMap'
    sheet_project.cell(row=irow, column=2).value = 'SocketMap'
    sheet_project.cell(row=irow, column=3).value = project_data[0][0][1][1]
    irow += 1
    if len(project_data[1][1]) > 0:
        sheet_project.cell(row=irow, column=1).value = 'Datalog'
        for i in range(len(project_data[1][1])):
            sheet_project.cell(row=irow, column=2).value = project_data[1][1][i][0]
            sheet_project.cell(row=irow, column=3).value = project_data[1][1][i][1]
            irow += 1
    sheet_project.merge_cells(start_row=2, end_row=irow - 1, start_column=1, end_column=1)
    if len(project_data[2][0]) > 0:
        start = irow
        sheet_project.cell(row=irow, column=1).value = 'ProjectSetup'
        for i in range(len(project_data[2][0])):
            sheet_project.cell(row=irow, column=2).value = project_data[2][0][i][0]
            sheet_project.cell(row=irow, column=3).value = project_data[2][0][i][1]
            irow += 1
        sheet_project.merge_cells(start_row=start, end_row=irow - 1, start_column=1, end_column=1)
    for row in sheet_project.rows:
        for cell in row:
            cell.border = border
            cell.alignment = alignment
            if cell.column in (1, 2):
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                if cell.row == 1:
                    cell.font = Font(color=RED, bold=True)
                else:
                    cell.font = Font(color=BLACK, bold=True)

    sheet_pinmap = wb.create_sheet('PinMap')
    sheet_pinmap.add_data_validation(dv_SignalType)
    dv_SignalType.add('G2:G1048576')
    sheet_pinmap.add_data_validation(dv_Unit)
    dv_Unit.add('K2:K1048576')
    dv_Unit.add('N2:N1048576')
    dv_Unit.add('Q2:Q1048576')
    sheet_pinmap.freeze_panes = 'B2'
    loadboard = [
        ['J21', 'J22', 'Seg 4_1/Site0', 'Seg 4_1/Site1'],
        ['J23', 'J24', 'Seg 5_1/Site2', 'Seg 5_1/Site3'],
        ['J9', 'J10', 'Seg 1_1/Site4', 'Seg 1_1/Site5'],
        ['J7', 'J8', 'Seg 0_1/Site6', 'Seg 0_1/Site7'],
        ['J17', 'J18', 'Seg 5_0/Site8', 'Seg 5_0/Site9'],
        ['J15', 'J16', 'Seg 4_0/Site10', 'Seg 4_0/Site11'],
        ['J1', 'J2', 'Seg 0_0/Site12', 'Seg 0_0/Site13'],
        ['J3', 'J4', 'Seg 1_0/Site14', 'Seg 1_0/Site15']
    ]
    HWPins = []
    for i in range(len(loadboard)):
        HWPins.append(
            [
                loadboard[i][2],
                ['PMU0', loadboard[i][0] + ': H_LCH00(PMU 0-31)', 'PMU0', 0],
                ['PMU1', loadboard[i][0] + ': H_LCH01(PMU 0-31)', 'PMU1', 1],
                ['PMU2', loadboard[i][0] + ': H_LCH02(PMU 0-31)', 'PMU2', 2],
                ['PMU3', loadboard[i][0] + ': H_LCH03(PMU 0-31)', 'PMU3', 3],
                ['PMU4', loadboard[i][0] + ': H_LCH04(PMU 0-31)', 'PMU4', 4],
                ['PMU5', loadboard[i][0] + ': H_LCH05(PMU 0-31)', 'PMU5', 5],
                ['PMU6/Mipi clk n', loadboard[i][0] + ': H_LCH12(PMU 0-31)/CH1_CSI_A_n', 'CSI_A_N_PMU12', 12],
                ['PMU7/Mipi clk p', loadboard[i][0] + ': H_LCH13(PMU 0-31)/CH1_CSI_A_p', 'CSI_A_P_PMU13', 13],
                ['PMU8/Mipi data0 n', loadboard[i][0] + ': H_LCH14(PMU 0-31)/CH1_CSI_B_n', 'CSI_B_N_PMU14', 14],
                ['PMU9/Mipi data0 p', loadboard[i][0] + ': H_LCH15(PMU 0-31)/CH1_CSI_B_p', 'CSI_B_P_PMU15', 15],
                ['PMU10/Mipi data1 n', loadboard[i][0] + ': H_LCH16(PMU 0-31)/CH1_CSI_C_n', 'CSI_C_N_PMU16', 16],
                ['PMU11/Mipi data1 p', loadboard[i][0] + ': H_LCH17(PMU 0-31)/CH1_CSI_C_p', 'CSI_C_P_PMU17', 17],
                ['PMU12/Mipi data2 n', loadboard[i][0] + ': H_LCH18(PMU 0-31)/CH1_CSI_D_n', 'CSI_D_N_PMU18', 18],
                ['PMU13/Mipi data2 p', loadboard[i][0] + ': H_LCH19(PMU 0-31)/CH1_CSI_D_p', 'CSI_D_P_PMU19', 19],
                ['PMU14/Mipi data3 n', loadboard[i][0] + ': H_LCH20(PMU 0-31)/CH1_CSI_E_n', 'CSI_E_N_PMU20', 20],
                ['PMU15/Mipi data3 p', loadboard[i][0] + ': H_LCH21(PMU 0-31)/CH1_CSI_E_p', 'CSI_E_P_PMU21', 21],
                ['PMU16', loadboard[i][1] + ': PE_E_S_0', 'PE_S0', 'M0'],
                ['PMU17', loadboard[i][1] + ': PE_E_S_1', 'PE_S1', 'M1'],
                ['PMU18', loadboard[i][1] + ': PE_E_S_2', 'PE_S2', 'M2'],
                ['PMU19', loadboard[i][1] + ': PE_E_S_3', 'PE_S3', 'M3'],
                ['PMU20', loadboard[i][1] + ': PE_E_S_4', 'PE_S4', 'M4'],
                ['PMU21', loadboard[i][1] + ': PE_E_S_5', '', 'M5'],
                ['PMU22', loadboard[i][1] + ': PE_E_S_6', '', 'M6'],
                ['PMU23', loadboard[i][1] + ': PE_E_S_7', '', 'M7'],
                ['DPS0', loadboard[i][1] + ': LVLC_F+_0', 'DPS_F0', 2000],
                ['DPS1', loadboard[i][1] + ': LVLC_F+_1', 'DPS_F1', 2001],
                ['DPS2', loadboard[i][1] + ': LVLC_F+_2', 'DPS_F2', 2002],
                ['DPS3', loadboard[i][1] + ': LVLC_F+_3', 'DPS_F3', 2003],
                ['GPIO1', loadboard[i][0] + ': gpio_3v3_2', '', 5065],
                ['GPIO2', loadboard[i][0] + ': gpio_3v3_5', '', 5068],
                ['GPIO3', loadboard[i][0] + ': gpio_3v3_6', '', 5069],
                ['GPIO4', 'gpio_2V5_0_p(Transition Board)', '', 5048],
                ['GPIO5', 'gpio_2V5_0_n(Transition Board)', '', 5049],
                ['GPIO6', 'gpio_2V5_1_p(Transition Board)', '', 5050],
                ['GPIO7', 'gpio_2V5_1_n(Transition Board)', '', 5051]
            ])
        HWPins.append(
            [
                loadboard[i][3],
                ['PMU0', loadboard[i][0] + ': H_LCH06(PMU 0-31)', 'PMU6', 6],
                ['PMU1', loadboard[i][0] + ': H_LCH07(PMU 0-31)', 'PMU7', 7],
                ['PMU2', loadboard[i][0] + ': H_LCH08(PMU 0-31)', 'PMU8', 8],
                ['PMU3', loadboard[i][0] + ': H_LCH09(PMU 0-31)', 'PMU9', 9],
                ['PMU4', loadboard[i][0] + ': H_LCH10(PMU 0-31)', 'PMU10', 10],
                ['PMU5', loadboard[i][0] + ': H_LCH11(PMU 0-31)', 'PMU11', 11],
                ['PMU6/Mipi clk n', loadboard[i][0] + ': H_LCH22(PMU 0-31)/CH1_CSI_A_n', 'CSI_A_N_PMU22', 22],
                ['PMU7/Mipi clk p', loadboard[i][0] + ': H_LCH23(PMU 0-31)/CH1_CSI_A_p', 'CSI_A_P_PMU23', 23],
                ['PMU8/Mipi data0 n', loadboard[i][0] + ': H_LCH24(PMU 0-31)/CH1_CSI_B_n', 'CSI_B_N_PMU24', 24],
                ['PMU9/Mipi data0 p', loadboard[i][0] + ': H_LCH25(PMU 0-31)/CH1_CSI_B_p', 'CSI_B_P_PMU25', 25],
                ['PMU10/Mipi data1 n', loadboard[i][0] + ': H_LCH26(PMU 0-31)/CH1_CSI_C_n', 'CSI_C_N_PMU26', 26],
                ['PMU11/Mipi data1 p', loadboard[i][0] + ': H_LCH27(PMU 0-31)/CH1_CSI_C_p', 'CSI_C_P_PMU27', 27],
                ['PMU12/Mipi data2 n', loadboard[i][0] + ': H_LCH28(PMU 0-31)/CH1_CSI_D_n', 'CSI_D_N_PMU28', 28],
                ['PMU13/Mipi data2 p', loadboard[i][0] + ': H_LCH29(PMU 0-31)/CH1_CSI_D_p', 'CSI_D_P_PMU29', 29],
                ['PMU14/Mipi data3 n', loadboard[i][0] + ': H_LCH30(PMU 0-31)/CH1_CSI_E_n', 'CSI_E_N_PMU30', 30],
                ['PMU15/Mipi data3 p', loadboard[i][0] + ': H_LCH31(PMU 0-31)/CH1_CSI_E_p', 'CSI_E_P_PMU31', 31],
                ['PMU16', loadboard[i][0] + ': PE_E_S_0_B', 'PE_S8', 'M8'],
                ['PMU17', loadboard[i][0] + ': PE_E_S_1_B', 'PE_S9', 'M9'],
                ['PMU18', loadboard[i][0] + ': PE_E_S_2_B', 'PE_S10', 'M10'],
                ['PMU19', loadboard[i][0] + ': PE_E_S_3_B', 'PE_S11', 'M11'],
                ['PMU20', loadboard[i][0] + ': PE_E_S_4_B', 'PE_S12', 'M12'],
                ['PMU21', loadboard[i][0] + ': PE_E_S_5_B', '', 'M13'],
                ['PMU22', loadboard[i][0] + ': PE_E_S_6_B', '', 'M14'],
                ['PMU23', loadboard[i][0] + ': PE_E_S_7_B', '', 'M15'],
                ['DPS0', loadboard[i][1] + ': LVLC_F+_4', 'DPS_F4', 2004],
                ['DPS1', loadboard[i][1] + ': LVLC_F+_5', 'DPS_F5', 2005],
                ['DPS2', loadboard[i][1] + ': LVLC_F+_6', 'DPS_F6', 2006],
                ['DPS3', loadboard[i][1] + ': LVLC_F+_7', 'DPS_F7', 2007],
                ['GPIO1', loadboard[i][0] + ': gpio_3v3_1', '', 5064],
                ['GPIO2', loadboard[i][0] + ': gpio_3v3_7', '', 5070],
                ['GPIO3', loadboard[i][0] + ': gpio_3v3_8', '', 5071],
                ['GPIO4', 'gpio_2V5_0_p(Transition Board)', '', 5048],
                ['GPIO5', 'gpio_2V5_0_n(Transition Board)', '', 5049],
                ['GPIO6', 'gpio_2V5_1_p(Transition Board)', '', 5050],
                ['GPIO7', 'gpio_2V5_1_n(Transition Board)', '', 5051]
            ]
        )

    pin_count = len(HWPins[0]) - 1
    irow = 1
    sheet_pinmap.cell(row=irow, column=1).value = 'Segment/Site'
    sheet_pinmap.cell(row=irow, column=2).value = 'Name'
    sheet_pinmap.cell(row=irow, column=3).value = 'LoadBoard Pin'
    sheet_pinmap.cell(row=irow, column=4).value = 'SocketBoard Pin'
    sheet_pinmap.cell(row=irow, column=6).value = 'PinName'
    sheet_pinmap.cell(row=irow, column=7).value = 'PinType'
    sheet_pinmap.merge_cells(start_row=1, end_row=1, start_column=9, end_column=11)
    sheet_pinmap.cell(row=irow, column=9).value = 'OS'
    sheet_pinmap.merge_cells(start_row=1, end_row=1, start_column=12, end_column=14)
    sheet_pinmap.cell(row=irow, column=12).value = 'IIL'
    sheet_pinmap.merge_cells(start_row=1, end_row=1, start_column=15, end_column=17)
    sheet_pinmap.cell(row=irow, column=15).value = 'IIH'
    irow += 1
    site_row = []
    used_limit = []
    for i in range(len(HWPins)):
        start = i * pin_count + i + 2
        end = (i + 1) * (pin_count + 1)
        site_row.append((start, end))
        sheet_pinmap.cell(row=irow, column=1).value = HWPins[i][0]
        for j in range(1, pin_count + 1):
            sheet_pinmap.cell(row=irow, column=2).value = HWPins[i][j][0]
            sheet_pinmap.cell(row=irow, column=3).value = HWPins[i][j][1]
            sheet_pinmap.cell(row=irow, column=4).value = HWPins[i][j][2]
            channel_id = str(HWPins[i][j][3])
            for m in range(len(socketmap_data)):
                socket_list = socketmap_data[m][1][0][1].split(' ')
                for socket in socket_list:
                    socket_channel_id = socket.split('.')[3]
                    if channel_id == socket_channel_id:
                        pin_name = socketmap_data[m][0][1]
                        sheet_pinmap.cell(row=irow, column=6).value = pin_name
                        for x in range(len(signals_data)):
                            if signals_data[x][0][1] == pin_name:
                                sheet_pinmap.cell(row=irow, column=7).value = signals_data[x][1][0][1]
                                break
                        for y in range(len(limit_data)):
                            if (limit_data[y][0][1].split('_')[0].upper() == pin_name and
                                        limit_data[y][0][1].split('_')[1].upper() == 'OS') \
                                    or (limit_data[y][0][1].split('_')[0].upper() == 'VN1' and pin_name == 'VN' and
                                                limit_data[y][0][1].split('_')[1].upper() == 'OS'):
                                used_limit.append(y)
                                sheet_pinmap.cell(row=irow, column=9).value = limit_data[y][1][2][1]
                                sheet_pinmap.cell(row=irow, column=10).value = limit_data[y][1][1][1]
                                sheet_pinmap.cell(row=irow, column=11).value = limit_data[y][1][3][1]
                            if limit_data[y][0][1].split('_')[0].upper() == pin_name and limit_data[y][0][1].split('_')[
                                1].upper() == 'IIL':
                                used_limit.append(y)
                                sheet_pinmap.cell(row=irow, column=12).value = limit_data[y][1][2][1]
                                sheet_pinmap.cell(row=irow, column=13).value = limit_data[y][1][1][1]
                                sheet_pinmap.cell(row=irow, column=14).value = limit_data[y][1][3][1]
                            if limit_data[y][0][1].split('_')[0].upper() == pin_name and limit_data[y][0][1].split('_')[
                                1].upper() == 'IIH':
                                used_limit.append(y)
                                sheet_pinmap.cell(row=irow, column=15).value = limit_data[y][1][2][1]
                                sheet_pinmap.cell(row=irow, column=16).value = limit_data[y][1][1][1]
                                sheet_pinmap.cell(row=irow, column=17).value = limit_data[y][1][3][1]
                        break
            irow += 1
        irow += 1
    used_limit = list(set(used_limit))
    for item in site_row:
        sheet_pinmap.merge_cells(start_row=item[0], end_row=item[1], start_column=1, end_column=1)

    for row in sheet_pinmap.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1 and cell.column not in (5, 8):
                cell.alignment = alignment
                cell.font = Font(color=RED, bold=True)
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
            if cell.column == 1:
                cell.alignment = alignment
            for item in site_row:
                if item[0] <= cell.row <= item[1]:
                    if cell.column == 2:
                        cell.font = Font(bold=True)
                    if 1 <= cell.column <= 4:
                        cell.fill = PatternFill(fill_type='solid', fgColor='CAE1FF')  # 浅蓝
                    if 6 <= cell.column <= 7 or cell.column >= 9:
                        cell.fill = PatternFill(fill_type='solid', fgColor='66CD00')  # 浅绿

    sheet_pingroup = wb.create_sheet('PinGroup')
    sheet_pingroup.add_data_validation(dv_SignalType)
    dv_SignalType.add('B2:B1048576')
    sheet_pingroup.freeze_panes = 'A2'
    irow = 1
    sheet_pingroup.cell(row=irow, column=1).value = 'PinGroup'
    sheet_pingroup.cell(row=irow, column=2).value = 'PinType'
    sheet_pingroup.cell(row=irow, column=3).value = 'Pins'
    irow += 1
    for i in range(len(signalgroups_data)):
        sheet_pingroup.cell(row=irow, column=1).value = signalgroups_data[i][0][1]
        sheet_pingroup.cell(row=irow, column=2).value = signalgroups_data[i][1][0][1]
        sheet_pingroup.cell(row=irow, column=3).value = signalgroups_data[i][1][1][1]
        irow += 1
    for row in sheet_pingroup.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1:
                cell.alignment = alignment
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                cell.font = Font(color=RED, bold=True)

    sheet_binmap = wb.create_sheet('BinMap')
    sheet_binmap.add_data_validation(dv_HWBinPassFail)
    dv_HWBinPassFail.add('H2:H1048576')
    sheet_binmap.freeze_panes = 'A2'
    irow = 1
    sheet_binmap.cell(row=irow, column=1).value = 'SWBinID'
    sheet_binmap.cell(row=irow, column=2).value = 'SWBinName'
    sheet_binmap.cell(row=irow, column=3).value = 'Comment'
    sheet_binmap.cell(row=irow, column=4).value = 'HWBinID'
    sheet_binmap.cell(row=irow, column=6).value = 'HWBinID'
    sheet_binmap.cell(row=irow, column=7).value = 'HWBinName'
    sheet_binmap.cell(row=irow, column=8).value = 'Pass/Fail'
    sheet_binmap.cell(row=irow, column=9).value = 'Comment'
    irow += 1
    for i in range(2, len(bindefinition_data[1])):
        sheet_binmap.cell(row=irow, column=1).value = bindefinition_data[1][i][1][0][1]
        sheet_binmap.cell(row=irow, column=2).value = bindefinition_data[1][i][0][1]
        sheet_binmap.cell(row=irow, column=3).value = bindefinition_data[1][i][1][1][1]
        hwbinname = bindefinition_data[1][i][1][2][1]
        for j in range(2, len(bindefinition_data[0])):
            if bindefinition_data[0][j][0][1] == hwbinname:
                sheet_binmap.cell(row=irow, column=4).value = bindefinition_data[0][j][1][0][1]
                if bindefinition_data[0][j][1][2][1] == 'Pass':
                    sheet_binmap.cell(row=irow, column=4).fill = PatternFill(fill_type='solid', fgColor=GREEN)
                else:
                    sheet_binmap.cell(row=irow, column=4).fill = PatternFill(fill_type='solid', fgColor=RED)
        irow += 1
    dv_SWBinId = DataValidation(type='list', formula1="{0}!$A$2:$A${1}".format(quote_sheetname('BinMap'), irow))
    irow = 2
    for i in range(2, len(bindefinition_data[0])):
        sheet_binmap.cell(row=irow, column=6).value = bindefinition_data[0][i][1][0][1]
        sheet_binmap.cell(row=irow, column=7).value = bindefinition_data[0][i][0][1]
        sheet_binmap.cell(row=irow, column=8).value = bindefinition_data[0][i][1][2][1]
        if bindefinition_data[0][i][1][2][1] == 'Pass':
            sheet_binmap.cell(row=irow, column=8).fill = PatternFill(fill_type='solid', fgColor=GREEN)
        else:
            sheet_binmap.cell(row=irow, column=8).fill = PatternFill(fill_type='solid', fgColor=RED)
        sheet_binmap.cell(row=irow, column=9).value = bindefinition_data[0][i][1][1][1]
        irow += 1
    dv_HWBinId = DataValidation(type='list', formula1="{0}!$F$2:$F${1}".format(quote_sheetname('BinMap'), irow))
    sheet_binmap.add_data_validation(dv_HWBinId)
    dv_HWBinId.add('D2:D1048576')
    for row in sheet_binmap.rows:
        for cell in row:
            cell.border = border
            cell.alignment = alignment
            if cell.row == 1 and cell.column != 5:
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                if cell.column == 3 or cell.column == 9:
                    cell.font = Font(color=BLACK, bold=True)
                else:
                    cell.font = Font(color=RED, bold=True)

    sheet_limits = wb.create_sheet('Limits')
    sheet_limits.add_data_validation(dv_Unit)
    dv_Unit.add('D2:D1048576')
    sheet_limits.add_data_validation(dv_SWBinId)
    dv_SWBinId.add('E2:E1048576')
    sheet_limits.freeze_panes = 'A2'
    irow = 1
    sheet_limits.cell(row=irow, column=1).value = 'Name'
    sheet_limits.cell(row=irow, column=2).value = 'HiLimit'
    sheet_limits.cell(row=irow, column=3).value = 'LoLimit'
    sheet_limits.cell(row=irow, column=4).value = 'Unit'
    sheet_limits.cell(row=irow, column=5).value = 'BinNum'
    sheet_limits.cell(row=irow, column=6).value = 'Comment'
    irow += 1
    for i in range(len(limit_data)):
        if i not in used_limit:
            sheet_limits.cell(row=irow, column=1).value = limit_data[i][0][1]
            sheet_limits.cell(row=irow, column=2).value = limit_data[i][1][2][1]
            sheet_limits.cell(row=irow, column=3).value = limit_data[i][1][1][1]
            if len(limit_data[i][1]) >= 4:
                sheet_limits.cell(row=irow, column=4).value = limit_data[i][1][3][1]
            if len(limit_data[i][1]) >= 5:
                sheet_limits.cell(row=irow, column=5).value = limit_data[i][1][4][1]
            if len(limit_data[i][1]) >= 6:
                sheet_limits.cell(row=irow, column=6).value = limit_data[i][1][5][1]
            irow += 1
    for row in sheet_limits.rows:
        for cell in row:
            cell.border = border
            if cell.row == 1:
                cell.alignment = alignment
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                if cell.column <= 4:
                    cell.font = Font(color=RED, bold=True)
                else:
                    cell.font = Font(color=BLACK, bold=True)

    sheet_dcmeasure = wb.create_sheet('DCMeasure')
    sheet_dcmeasure.add_data_validation(dv_sigref)
    dv_sigref.add('B2:B1048576')
    sheet_dcmeasure.add_data_validation(dv_MeasureModeType)
    dv_MeasureModeType.add('D2:D1048576')
    sheet_dcmeasure.add_data_validation(dv_MeasureMethodType)
    dv_MeasureMethodType.add('E2:E1048576')
    sheet_dcmeasure.freeze_panes = 'A2'
    irow = 1
    sheet_dcmeasure.cell(row=irow, column=1).value = 'DCMeasure'
    sheet_dcmeasure.cell(row=irow, column=2).value = 'Signal'
    sheet_dcmeasure.cell(row=irow, column=3).value = 'minorTestNum'
    sheet_dcmeasure.cell(row=irow, column=4).value = 'Mode'
    sheet_dcmeasure.cell(row=irow, column=5).value = 'Method'
    sheet_dcmeasure.cell(row=irow, column=6).value = 'ForceValue'
    sheet_dcmeasure.cell(row=irow, column=7).value = 'IRange'
    sheet_dcmeasure.cell(row=irow, column=8).value = 'HiLimit'
    sheet_dcmeasure.cell(row=irow, column=9).value = 'LoLimit'
    sheet_dcmeasure.cell(row=irow, column=10).value = 'HiClamp'
    sheet_dcmeasure.cell(row=irow, column=11).value = 'LoClamp'
    sheet_dcmeasure.cell(row=irow, column=12).value = 'SampleNum'
    sheet_dcmeasure.cell(row=irow, column=13).value = 'Delay'
    irow += 1
    for i in range(len(dcmeasure_data)):
        sheet_dcmeasure.cell(row=irow, column=1).value = dcmeasure_data[i][0][1]
        for j in range(1, len(dcmeasure_data[i])):
            sheet_dcmeasure.cell(row=irow, column=2).value = dcmeasure_data[i][j][0][1]
            sheet_dcmeasure.cell(row=irow, column=3).value = dcmeasure_data[i][j][1][1]
            sheet_dcmeasure.cell(row=irow, column=4).value = dcmeasure_data[i][j][2][0][1]
            sheet_dcmeasure.cell(row=irow, column=5).value = dcmeasure_data[i][j][2][1][1]
            sheet_dcmeasure.cell(row=irow, column=6).value = dcmeasure_data[i][j][2][2][1]
            sheet_dcmeasure.cell(row=irow, column=7).value = dcmeasure_data[i][j][2][3][1]
            sheet_dcmeasure.cell(row=irow, column=8).value = dcmeasure_data[i][j][2][4][1]
            sheet_dcmeasure.cell(row=irow, column=9).value = dcmeasure_data[i][j][2][5][1]
            sheet_dcmeasure.cell(row=irow, column=10).value = dcmeasure_data[i][j][2][6][1]
            sheet_dcmeasure.cell(row=irow, column=11).value = dcmeasure_data[i][j][2][7][1]
            sheet_dcmeasure.cell(row=irow, column=12).value = dcmeasure_data[i][j][2][8][1]
            sheet_dcmeasure.cell(row=irow, column=13).value = dcmeasure_data[i][j][2][9][1]
            irow += 1
        irow += 1
    for row in sheet_dcmeasure.rows:
        for cell in row:
            cell.border = border
            cell.alignment = alignment
            if cell.row == 1:
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                cell.font = Font(color=RED, bold=True)

    sheet_test = wb.create_sheet('Test')
    sheet_test.freeze_panes = 'A2'
    irow = 1
    sheet_test.cell(row=irow, column=1).value = 'Test Item'
    sheet_test.cell(row=irow, column=2).value = 'TestNum'
    sheet_test.cell(row=irow, column=3).value = 'ExecAPI'
    irow += 1
    param_count = 0
    for i in range(len(tests_data)):
        sheet_test.cell(row=irow, column=1).value = tests_data[i][0][1]
        sheet_test.cell(row=irow, column=2).value = tests_data[i][1][1]
        sheet_test.cell(row=irow, column=3).value = tests_data[i][-1][1][1]
        temp_count = len(tests_data[i]) - 3
        if param_count < temp_count:
            param_count = temp_count
        for j in range(temp_count):
            para = tests_data[i][2 + j][0][1] + ':' + tests_data[i][2 + j][1][1][1]
            sheet_test.cell(row=irow, column=(4 + j)).value = para
        irow += 1
    for i in range(param_count):
        sheet_test.cell(row=1, column=(4 + i)).value = 'Param' + str(i)
    for row in sheet_test.rows:
        for cell in row:
            cell.border = border
            cell.alignment = alignment
            if cell.row == 1:
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                if cell.column in (1, 2, 3):
                    cell.font = Font(color=RED, bold=True)
                else:
                    cell.font = Font(color=BLACK, bold=True)

    sheet_uservars = wb.create_sheet('UserVars')
    sheet_uservars.add_data_validation(dv_VariableType)
    dv_VariableType.add('B2:B1048576')
    sheet_uservars.freeze_panes = 'A2'
    irow = 1
    sheet_uservars.cell(row=irow, column=1).value = 'UserVars'
    sheet_uservars.cell(row=irow, column=2).value = 'Type'
    sheet_uservars.cell(row=irow, column=3).value = 'Val'
    irow += 1
    for i in range(len(uservars_data)):
        sheet_uservars.cell(row=irow, column=1).value = uservars_data[i][0][1]
        sheet_uservars.cell(row=irow, column=2).value = uservars_data[i][1][1]
        sheet_uservars.cell(row=irow, column=3).value = uservars_data[i][2][0][1]
        irow += 1
    for row in sheet_uservars.rows:
        for cell in row:
            cell.border = border
            cell.alignment = alignment
            if cell.row == 1:
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                cell.font = Font(color=RED, bold=True)

    sheet_level = wb.create_sheet('Level')
    sheet_level.add_data_validation(dv_sigref)
    dv_sigref.add('B2:B1048576')
    sheet_level.freeze_panes = 'A2'
    irow = 1
    level_title = ['LevelName', 'SigRef', 'VPS', 'IClamp', 'IRange', 'Delay', 'VIL', 'VIH', 'VTERM', 'VTERM_EN', 'VOL',
                   'VOH', 'VCH', 'VCL']
    for i in range(len(level_title)):
        sheet_level.cell(row=irow, column=(1 + i)).value = level_title[i]
    irow += 1
    for i in range(len(levels_data)):
        sheet_level.cell(row=irow, column=1).value = levels_data[i][0][1]
        for j in range(1, len(levels_data[i])):
            sheet_level.cell(row=irow, column=2).value = levels_data[i][j][0][1]
            for m in range(len(levels_data[i][j][1])):
                col = level_title.index(levels_data[i][j][1][m][0])
                sheet_level.cell(row=irow, column=(1 + col)).value = levels_data[i][j][1][m][1]
            irow += 1
        irow += 1
    for row in sheet_level.rows:
        for cell in row:
            cell.border = border
            cell.alignment = alignment
            if cell.row == 1:
                cell.fill = PatternFill(fill_type='solid', fgColor=YELLOW)
                if cell.column in (1, 2):
                    cell.font = Font(color=RED, bold=True)
                elif cell.column in (3, 4, 5, 6):
                    cell.font = Font(color='00CCCC', bold=True)  # 蓝色
                else:
                    cell.font = Font(color='666633', bold=True)  # 褐色

    for sheet_name in wb.sheetnames:
        if sheet_name == 'Sheet':
            del wb[sheet_name]
        else:
            Common.set_column_width(wb[sheet_name])

    print("保存数据开始-----------------")
    wb.save(file_name)
    print("保存数据结束-----------------")


def main():
    # Project folder path
    if argv.count('-p') == 0:
        print("Error：Project folder path 格式：“-p D:\Project” 。")
        exit()
    else:
        project_folder = argv[argv.index('-p') + 1]
        project_data = read_project(project_folder)
        socketmap_data = read_socketmap(project_folder)
        signals_data = read_signals(project_folder)
        limit_data = read_limit(project_folder)
        signalgroups_data = read_signalgroups(project_folder)
        bindefinition_data = read_bindefinition(project_folder)
        dcmeasure_data = read_dcmeasure(project_folder)
        tests_data = read_tests(project_folder)
        uservars_data = read_uservars(project_folder)
        levels_data = read_levels(project_folder)
    write_excel(project_data, socketmap_data, signals_data, limit_data, signalgroups_data, bindefinition_data,
                dcmeasure_data, tests_data, uservars_data, levels_data)


if __name__ == '__main__':
    main()
