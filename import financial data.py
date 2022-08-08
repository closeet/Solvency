import pandas
import os
import static_parameters
import database
import database_setting
import time
import math


def ls_to_dict_nonreplica(ls_key: list, ls_value: list):
    ls_key_nonreplica = []
    ls_value_nonreplica = []
    for index, key in enumerate(ls_key):
        if key not in ls_key_nonreplica:
            ls_key_nonreplica.append(key)
            ls_value_nonreplica.append(ls_value[index])
        else:
            ls_value_nonreplica[ls_key_nonreplica.index(key)] += ls_value[index]

    return dict(zip(ls_key_nonreplica, ls_value_nonreplica))


def read_bs_sheet(path):
    ws = pandas.read_excel(path, sheet_name='资产负债表')
    dict_bs_asset = {ws.iloc[row_num, 0].replace(" ", ""): ws.iloc[row_num, 2] for row_num in range(ws.shape[0]) if
                     isinstance(ws.iloc[row_num, 0], str) and ws.iloc[row_num, 0].replace(" ",
                                                                                          "") in static_parameters.ls_bs_subject}
    dict_bs_liab_equity = {ws.iloc[row_num, 3].replace(" ", ""): ws.iloc[row_num, 5] for row_num in
                           range(ws.shape[0]) if
                           isinstance(ws.iloc[row_num, 3], str) and ws.iloc[row_num, 3].replace(" ",
                                                                                                "") in static_parameters.ls_bs_subject}
    dict_bs_raw = dict(**dict_bs_asset, **dict_bs_liab_equity)

    for key, value in dict_bs_raw.items():
        if value != value:
            dict_bs_raw[key] = 0
    dict_bs = {}
    for subject in static_parameters.ls_bs_subject:
        if subject in dict_bs_raw:
            dict_bs[subject] = dict_bs_raw[subject]
        else:
            dict_bs[subject] = 0
    return dict_bs


def read_subject_sheet(path):
    ws = pandas.read_excel(path, sheet_name=3)
    for row in range(ws.shape[0]):
        if ws.iloc[row, 0] == '1001':
            start_row = row
            break
    ls_subject_code = [ws.iloc[row_num, 0] for row_num in range(start_row, ws.shape[0])]
    ls_subject_name = [ws.iloc[row_num, 1] for row_num in range(start_row, ws.shape[0])]
    ls_subject_value_raw = [ws.iloc[row_num, 5] for row_num in range(start_row, ws.shape[0])]
    ls_subject_value = []
    for value in ls_subject_value_raw:
        if isinstance(value, str):
            ls_subject_value.append(float(value.replace(",", "")))
        else:
            ls_subject_value.append(value)
    ls_index_4 = [ls_subject_code.index(code) for code in ls_subject_code if len(code) == 4]
    ls_name_4 = [ls_subject_name[index] for index in ls_index_4]
    ls_value_4 = [ls_subject_value[index] for index in ls_index_4]
    dict_subject_4_digit_raw = ls_to_dict_nonreplica(ls_name_4, ls_value_4)
    ls_index_6 = [ls_subject_code.index(code) for code in ls_subject_code if len(code) == 6]
    ls_name_6 = [ls_subject_name[index] for index in ls_index_6]
    ls_value_6 = [ls_subject_value[index] for index in ls_index_6]
    dict_subject_6_digit_raw = ls_to_dict_nonreplica(ls_name_6, ls_value_6)
    dict_subject_4_digit = {}
    dict_subject_6_digit = {}
    for subject in static_parameters.ls_subject_detail_1:
        if subject in dict_subject_4_digit_raw:
            dict_subject_4_digit[subject] = dict_subject_4_digit_raw[subject]
        else:
            dict_subject_4_digit[subject] = 0
    for subject in static_parameters.ls_subject_detail_2:
        if subject in dict_subject_6_digit_raw:
            dict_subject_6_digit[subject] = dict_subject_6_digit_raw[subject]
        else:
            dict_subject_6_digit[subject] = 0
    return [dict_subject_4_digit, dict_subject_6_digit]


dict_bs_data = {}
dict_subject_4_data = {}
dict_subject_6_data = {}
ls_bs_data = []
ls_subject_data_4 = []
ls_subject_data_6 = []
for root, dirs, files in os.walk('财报'):
    for name in files:
        if name.split('.')[1].find('xls') + 1:
            file_time_fin = name.split('年')[0] + name.split('年')[1].split('月')[0].rjust(2, '0')

            file_path_fin = os.path.join(root, name)
            bs_data = read_bs_sheet(file_path_fin)
            dict_bs_data[file_time_fin] = bs_data

            ls_bs = [int(file_time_fin), int(file_time_fin[:4]), int(file_time_fin[4:]), *bs_data.values()]
            for data in ls_bs:
                if data != data:
                    data = 0
            ls_bs_data.append(ls_bs)
            subject_data = read_subject_sheet(file_path_fin)
            dict_subject_4_data[file_time_fin] = subject_data[0]
            dict_subject_6_data[file_time_fin] = subject_data[1]
            ls_subject_4 = [int(file_time_fin), int(file_time_fin[:4]), int(file_time_fin[4:]),
                            *subject_data[0].values()]
            ls_subject_6 = [int(file_time_fin), int(file_time_fin[:4]), int(file_time_fin[4:]),
                            *subject_data[1].values()]
            ls_subject_data_4.append(ls_subject_4)
            ls_subject_data_6.append(ls_subject_6)

ls_bs_data.sort(key=lambda x: x[0])
ls_subject_data_4.sort(key=lambda x: x[0])
ls_subject_data_6.sort(key=lambda x: x[0])

ls_col_name_bs = ['评估时点', '年份', '月份', *static_parameters.ls_bs_subject]
ls_col_name_subject_4 = ['评估时点', '年份', '月份', *static_parameters.ls_subject_detail_1]
ls_col_name_subject_6 = ['评估时点', '年份', '月份', *static_parameters.ls_subject_detail_2]

db_fin = database.MySqlConnection(*database_setting.ls_setting_solvency)
# time_start = time.time()
# print('正在导入计算结果......')

db_fin.insert('资产负债表', ls_col_name_bs, ls_bs_data)
db_fin.insert('一级科目余额表', ls_col_name_subject_4, ls_subject_data_4)
db_fin.insert('二级科目余额表', ls_col_name_subject_6, ls_subject_data_6)



