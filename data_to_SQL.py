from data_import import ls_sd_data, ls_col_sd_data, ls_col_labeled_data, ls_labeled_data, ls_data_before_penetration, ls_col_before_penetration
from database import *
import time
from database_setting import ls_setting_asset
db_solv = MySqlConnection(*ls_setting_asset)


def data_to_sql():
    time_start = time.time()
    print('正在导入清洗后数据......')

    if db_solv.sql_query("select count(*) from information_schema.TABLES where table_name = '"+table_name_raw+"'")[0][0]:
        db_solv.sql_exec(sql_drop_table_raw)
    db_solv.sql_exec(sql_create_table_raw)

    if db_solv.sql_query("select count(*) from information_schema.TABLES where table_name = '" + table_name_labeled + "'")[0][0]:
        db_solv.sql_exec(sql_drop_table_labeled)
    db_solv.sql_exec(sql_create_table_labeled)

    if db_solv.sql_query("select count(*) from information_schema.TABLES where table_name = '" + table_name_asset + "'")[0][0]:
        db_solv.sql_exec(sql_drop_table_asset)
    db_solv.sql_exec(sql_create_table_asset)

    db_solv.insert(table_name_raw, ls_col_sd_data, ls_sd_data)
    db_solv.insert(table_name_labeled, ls_col_labeled_data, ls_labeled_data)
    db_solv.insert(table_name_asset, ls_col_before_penetration, ls_data_before_penetration)

    time_end = time.time()
    print('导入原始数据用时{}秒'.format(time_end - time_start))



