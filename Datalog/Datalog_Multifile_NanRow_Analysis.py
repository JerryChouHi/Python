# encoding:utf-8
# @Time     : 2019/9/11
# @Author   : Jerry Chou
# @File     :
# @Function : 1、多文件分析  2、分析空值的行
import datetime
import pandas, os
from sys import argv

row_offset = 5
col_offset = 4
last_dc_testitem = 'PWDN_Total'


def get_nan_row(df):
    """
    获得有空值的行的列表
    :param df: 
    :return: 
    """
    exist_nan_row = df[df.isnull().T.any()]
    exist_nan_row_list = list(exist_nan_row.index.values)
    return exist_nan_row_list


def parse_file(file, result_file):
    try:
        read_file = pandas.read_csv(file, na_values=' ')
    except Exception as e:
        print(e)

    for indexs in read_file.index:
        for i in range(len(read_file.iloc[indexs].values)):
            if read_file.iloc[indexs].values[i] == last_dc_testitem:
                pwdn_total_row_num = indexs
                pwdn_total_col_num = i
                break
        else:
            continue
        break
    chipnum_df = read_file.iloc[pwdn_total_row_num + row_offset:, 0]
    for chipnum in chipnum_df:
        try:
            int(chipnum)
        except:
            FirstRegister = chipnum
            break
    firstregister_row_num = read_file[read_file.iloc[:, 0].isin([FirstRegister])].index[0]

    dc_df = read_file.iloc[pwdn_total_row_num + row_offset:firstregister_row_num, 0:pwdn_total_col_num + 1]
    image_df = read_file.iloc[pwdn_total_row_num + row_offset:firstregister_row_num,
               pwdn_total_col_num + 1:read_file.shape[1] - 2]

    dc_nan_row = [i + 2 for i in get_nan_row(dc_df)]
    image_nan_row = [i + 2 for i in get_nan_row(image_df)]
    with open(result_file, 'a') as f:
        f.write(file + " 存在空值的行：\n")
        f.write("(1) DC 共 " + str(len(dc_nan_row)) + " 行，它们是:" + str(dc_nan_row) + "\n")
        f.write("(2) IMAGE 共 " + str(len(image_nan_row)) + " 行，它们是:" + str(image_nan_row) + '\n')


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
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    result_file = os.path.join(analysis_folder, 'NanRow_Analysis' + date + '.txt')

    for file in file_list:
        original_file = os.path.join(sourcefile_folder, file)
        # parse file
        parse_file(original_file, result_file)


if __name__ == '__main__':
    main()
