from data_import import data_deposit, data_current_deposit, data_invest_asset
from Data_Manipulation import AssetData
from database import MySqlConnection
import time
# time_start = time.time()
sb_solv = MySqlConnection(host="localhost", user="root", password="19981027phy", database="solvency2")

# for i in data_invest_asset.keys():
#     asset = AssetData(data_invest_asset[i])
#     asset.data_check()
#     sb_solv.insert("data_raw", asset.sd_data.keys(), list(asset.sd_data.values()))
#     sb_solv.close()
# time_end = time.time()
# print('用时{}秒'.format(time_end - time_start))

a = sb_solv.sb_query("SELECT * FROM solvency2.data_raw;")
print(a.fetchall())
