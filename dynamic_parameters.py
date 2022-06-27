from database import MySqlConnection
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


def stock_k1(ls_price, ls_cost):
    if sum(ls_cost):
        x = (sum(ls_price) - sum(ls_cost)) / sum(ls_cost)
        if x >= 1:
            return 1
        elif 0 <= x < 1:
            return x ** 2
        elif -1 <= x < 0:
            return -(x ** 2)
        else:
            return -1
    else:
        return 0

"""---------------------------------"""
ls_stock_price = []
ls_stock_cost = []
"""---------------------------------"""
dict_k1 = {'涨跌幅': stock_k1(ls_stock_price, ls_stock_cost), '地区': 0.2, '市场类型': 0.25, '绿债': -0.1}

