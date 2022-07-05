from data_import import *
from Class_min_capital import MinCapital
from database import *
import time
from database_setting import *
from dynamic_parameters import *


time_start = time.time()

ls_calc_data = []
for data in ls_dict_sd_data:
    mc = MinCapital(data)
    ls_calc_data.append(list(mc.calc_data.values()))
ls_col_calc_data = list(mc.calc_data.keys())

db_solv = MySqlConnection(host=db_host, user=db_user, password=db_password, database=db_database)

if __name__ == '__main__':
    if db_solv.sql_query("select count(*) from information_schema.TABLES where table_name = '" + table_name_calc + "'")[0][0]:
        db_solv.sql_exec(sql_drop_table_calc)
    db_solv.sql_exec(sql_create_table_clac)
    db_solv.insert(table_name_calc, ls_col_calc_data, ls_calc_data)

time_end = time.time()
print('用时{}秒'.format(time_end - time_start))
