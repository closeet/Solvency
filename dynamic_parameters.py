from database import MySqlConnection
from data_to_SQL import sb_solv


def concentration_counter_party_threshold(total_asset):
    tier1 = 10000000000
    tier2 = 50000000000
    tier3 = 100000000000
    tier0 = 500000000
    if total_asset <= tier0:
        return 10 ** 20
    else:
        return (total_asset > tier3) * (total_asset - tier3) * 0.03 \
               + (total_asset > tier2) * min(tier3, total_asset) * 0.04 \
               + (total_asset > tier1) * min(tier2, total_asset) * 0.05 \
               + min(tier1, total_asset) * 0.08


def concentration_asset_type_threshold(total_asset_last_quarter, dict_asset_type_proportion: dict):
    return {'权益': total_asset_last_quarter * dict_asset_type_proportion['权益'],
            '房地产': total_asset_last_quarter * dict_asset_type_proportion['房地产'],
            '其他': total_asset_last_quarter * dict_asset_type_proportion['其他'],
            '境外': total_asset_last_quarter * dict_asset_type_proportion['境外']
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


total_asset = 374129517345.931


sum_price_stock = sb_solv.sb_query("SELECT sum(`认可价值`) FROM solvency2.data_raw where `资产大类`='股票' and `表层资产简称`is null;")[0][0]
sum_cost_stock = sb_solv.sb_query("SELECT sum(`购买成本`) FROM solvency2.data_raw where `资产大类`='股票' and `表层资产简称`is null;")[0][0]
counter_party_all = sb_solv.sb_query("select `交易对手`, sum(`认可价值`) FROM solvency2.data_raw group by `交易对手` order by sum(`认可价值`) desc")
asset_type_all = sb_solv.sb_query("select `资产五大类分类`, sum(`认可价值`) FROM solvency2.data_raw group by `资产五大类分类` order by sum(`认可价值`) desc")
ls_counter_party = [counter_party_all[i][0] for i in range(len(counter_party_all)) if counter_party_all[i][1]>=concentration_counter_party_threshold(total_asset)]

dict_k1 = {'涨跌幅': stock_k1(sum_price_stock, sum_cost_stock), '地区': 0.2, '市场类型': 0.25, '绿债': -0.1}

