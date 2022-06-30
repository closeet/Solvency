from data_import import data_deposit, data_current_deposit, data_invest_asset
from Class_asset_data import AssetData
from database import *
import time

time_start = time.time()
# sb_solv = MySqlConnection(host="localhost", user="root", password="19981027phy", database="solvency2")
db_solv = MySqlConnection(host="localhost", user="root", password="19981027Phy", database="solvency_data")
bool1 = 1
if __name__ == '__main__':
    if db_solv.sql_query("select count(*) from information_schema.TABLES where table_name = '"+table_name_raw+"'")[0][0]:
        db_solv.sql_exec(sql_drop_table_raw)
    db_solv.sql_exec(sql_create_table_raw)

    if db_solv.sql_query("select count(*) from information_schema.TABLES where table_name = '" + table_name_labeled + "'")[0][0]:
        db_solv.sql_exec(sql_drop_table_labeled)
    db_solv.sql_exec(sql_create_table_labeled)

    for i in data_invest_asset.keys():
        asset = AssetData(data_invest_asset[i])
        db_solv.insert(table_name_raw, asset.sd_data.keys(), list(asset.sd_data.values()))
        db_solv.insert(table_name_labeled, asset.labeled_data.keys(), list(asset.labeled_data.values()))
        # db_solv.close()
    time_end = time.time()
    print('用时{}秒'.format(time_end - time_start))

# print(data_invest_asset[6])

    # a = sb_solv.sql_query("SELECT sum(`认可价值`) FROM solvency2.data_raw where `资产大类`='股票' and `表层资产简称`is null;")
    # print(a.fetchall())

