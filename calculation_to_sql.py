from data_import import *
from Class_min_capital import MinCapital
from database import *
import time
from database_setting import ls_setting_asset
from dynamic_parameters import *


def calc_to_sql():
    time_start = time.time()
    print('正在计算最低资本......')
    ls_calc_data = []
    for data in ls_dict_sd_data:
        mc = MinCapital(data)
        ls_calc_data.append(list(mc.calc_data.values()))
    ls_col_calc_data = list(mc.calc_data.keys())
    time_end = time.time()
    print('计算最低资本用时{}秒'.format(time_end - time_start))
    db_solv = MySqlConnection(*ls_setting_asset)

    time_start = time.time()
    print('正在导入计算结果......')
    if db_solv.sql_query("select count(*) from information_schema.TABLES where table_name = '" + table_name_calc + "'")[0][0]:
        db_solv.sql_exec(sql_drop_table_calc)
    db_solv.sql_exec(sql_create_table_clac)
    db_solv.insert(table_name_calc, ls_col_calc_data, ls_calc_data)

    time_end = time.time()
    print('导入计算结果用时{}秒'.format(time_end - time_start))
