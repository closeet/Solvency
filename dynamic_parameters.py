from database import table_name_raw, table_name_labeled
from data_to_SQL import db_solv
from static_parameters import *
from database_setting import *
from database import evaluate_year, evaluate_month
from data_import import dict_asset_type_concentration
import pandas


def concentration_counter_party_threshold(total_asset):
    tier1 = 10000000000
    tier2 = 50000000000
    tier3 = 100000000000
    tier0 = 500000000
    if total_asset <= tier0:
        return 10 ** 20
    else:
        return (total_asset > tier3) * (total_asset - tier3) * 0.03 \
               + (total_asset > tier2) * min(tier3-tier2, total_asset-tier2) * 0.04 \
               + (total_asset > tier1) * min(tier2-tier1, total_asset-tier1) * 0.05 \
               + min(tier1, total_asset) * 0.08


def concentration_asset_type_threshold(total_asset_last_quarter, dict_asset_type_proportion: dict):
    return {'权益类资产': total_asset_last_quarter * dict_asset_type_proportion['权益'],
            '不动产类资产': total_asset_last_quarter * dict_asset_type_proportion['房地产'],
            '其他金融资产': total_asset_last_quarter * dict_asset_type_proportion['其他'],
            '境外资产': total_asset_last_quarter * dict_asset_type_proportion['境外']
            }


def stock_k1(price, cost):
    x = (price - cost) / cost
    if x >= 1:
        return 1
    elif 0 <= x < 1:
        return x ** 2
    elif -1 <= x < 0:
        return -(x ** 2)
    else:
        return -1


total_asset = pandas.read_excel('财报/'+evaluate_year+'/'+evaluate_year+'年'+evaluate_month+'月和谐健康财务报表.xls', sheet_name='资产负债表').iloc[45, 2]
if int(evaluate_month) <= 3:
    last_q_year = str(int(evaluate_year)-1)
    last_q_month = '12'
else:
    last_q_year = evaluate_year
    last_q_month = str(((int(evaluate_month)-1) // 3)*3)
total_asset_last_quarter = pandas.read_excel('财报/'+last_q_year+'/'+last_q_year+'年'+last_q_month+'月和谐健康财务报表.xls', sheet_name='资产负债表').iloc[45, 2] - \
                           pandas.read_excel('财报/'+last_q_year+'/'+last_q_year+'年'+last_q_month+'月和谐健康财务报表.xls', sheet_name='资产负债表').iloc[8, 5]


sum_price_stock = db_solv.sql_query("SELECT sum(`认可价值`) FROM " + db_database_asset + "." + table_name_raw + " where `资产大类`='股票' and `表层资产简称`is null;")[0][0]
sum_cost_stock = db_solv.sql_query("SELECT sum(`购买成本`) FROM " + db_database_asset + "." + table_name_raw + " where `资产大类`='股票' and `表层资产简称`is null;")[0][0]
counter_party_all = db_solv.sql_query("select `交易对手`, sum(`认可价值`) FROM " + db_database_asset + "." + table_name_raw + " group by `交易对手` order by sum(`认可价值`) desc")
ls_counter_party = [counter_party_all[i][0] for i in range(len(counter_party_all)) if counter_party_all[i][1]>=concentration_counter_party_threshold(total_asset)]
print(concentration_counter_party_threshold(total_asset))
print(concentration_asset_type_threshold(total_asset_last_quarter, dict_asset_type_proportion).keys())
sum_foreign_asset = db_solv.sql_query("select sum from (select `境内外`, sum(`认可价值`) as sum from " + db_database_asset + "." +
                                      table_name_labeled + " where `是否穿透` = '未穿透' group by `境内外`) a where `境内外` = '境外';")[0][0]
dict_k1 = {'涨跌幅': stock_k1(sum_price_stock, sum_cost_stock), '地区': 0.2, '市场类型': 0.25, '绿债': -0.1}
dict_asset_type_all = dict_asset_type_concentration
dict_asset_type_all['境外资产'] = sum_foreign_asset
ls_asset_type = [type_asset for type_asset in concentration_asset_type_threshold(total_asset_last_quarter,
                                                                                    dict_asset_type_proportion).keys()
                 if type_asset in dict_asset_type_all.keys() and concentration_asset_type_threshold(total_asset_last_quarter, dict_asset_type_proportion)
                 [type_asset] < dict_asset_type_all[type_asset]]
