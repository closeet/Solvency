from data_import import data_deposit, data_current_deposit, data_invest_asset
from Class_min_capital import MinCapital
from database import *
import time

asset_data_1 = data_invest_asset[6]
mc = MinCapital(asset_data_1)

# for i in data_invest_asset.keys():
#     asset = MinCapital(data_invest_asset[i])
#     print(asset.calc_data)
time_start = time.time()
# sb_solv = MySqlConnection(host="localhost", user="root", password="19981027phy", database="solvency2")
db_solv = MySqlConnection(host="localhost", user="root", password="19981027Phy", database="solvency_data")
bool1 = 1
if __name__ == '__main__':
    if db_solv.sql_query("select count(*) from information_schema.TABLES where table_name = '"+table_name_calc+"'")[0][0]:
        db_solv.sql_exec(sql_delete_table_calc)
    else:
        db_solv.sql_exec(sql_create_table_clac)

    for i in data_invest_asset.keys():
        asset = MinCapital(data_invest_asset[i])
        print(asset.calc_data)
        db_solv.insert(table_name_calc, asset.calc_data.keys(), list(asset.calc_data.values()))

        # db_solv.close()
    db_solv.close()
    time_end = time.time()
    print('用时{}秒'.format(time_end - time_start))
