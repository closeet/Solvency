from data_import import *
from Class_asset_data import AssetData
from database import *
import time
from database_setting import *

time_start = time.time()

db_solv = MySqlConnection(host=db_host, user=db_user, password=db_password, database=db_database)
# db_solv = MySqlConnection(host="localhost", user="root", password="19981027Phy", database="solvency_data")
bool1 = 1
if __name__ == '__main__':
    if db_solv.sql_query("select count(*) from information_schema.TABLES where table_name = '"+table_name_raw+"'")[0][0]:
        db_solv.sql_exec(sql_drop_table_raw)
    db_solv.sql_exec(sql_create_table_raw)

    if db_solv.sql_query("select count(*) from information_schema.TABLES where table_name = '" + table_name_labeled + "'")[0][0]:
        db_solv.sql_exec(sql_drop_table_labeled)
    db_solv.sql_exec(sql_create_table_labeled)

    db_solv.insert(table_name_raw, ls_col_sd_data, ls_sd_data)
    db_solv.insert(table_name_labeled, ls_col_labeled_data, ls_labeled_data)
    # print(lsa[-1:])
    # db_solv.close()
time_end = time.time()
print('用时{}秒'.format(time_end - time_start))

# print(data_invest_asset[6])

    # a = sb_solv.sql_query("SELECT sum(`认可价值`) FROM solvency2.data_raw where `资产大类`='股票' and `表层资产简称`is null;")
    # print(a.fetchall())

