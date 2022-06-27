import openpyxl
import pickle
from process_values import ws_cell
from process_values import max_row
from dynamic_parameters import stock_k1


def serialize(ls, filename):
    with open(filename, 'wb') as file:
        pickle.dump(ls, file)


def deserialize(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


wb_data_rule = openpyxl.load_workbook('数据规则.xlsx')
ws_rule_bank = wb_data_rule['存款交易对手']
ws_rule_null = wb_data_rule['字段空与非空']
ws_rule_type = wb_data_rule['数据类型']
ws_rule_valid = wb_data_rule['字段取值']
ws_rule_k = wb_data_rule['k1,k2']
ws_rule_others = wb_data_rule['其他']

dict_deposit_col_name_self = {'购买成本': '存款金额', '认可价值': '认可价值', '应收利息': '应收利息', '存款银行类型': '银行类型', '资产类型': '存款类型'}
ls_deposit_col_name = ['资产简称', '资产全称', '资产大类', '资产类型', '交易对手', '购买成本', '认可价值', '应收利息', '账户', '存款银行类型', '银行资本充足率',
                       '资产五大类分类']
dict_current_deposit_col_name_self = {'资产简称': '帐户信息', '资产全称': '帐户信息', '购买成本': '余额', '认可价值': '余额'}
dict_current_deposit_col_value = {'资产大类': '现金及流动性管理工具', '资产类型': '活期存款', '资产五大类分类': '流动性资产'}

ls_current_deposit = ['资产简称', '资产全称', '资产大类', '资产类型', '交易对手', '购买成本', '认可价值', '账户', '资产五大类分类']

dict_bank_counter_party = {ws_cell(ws_rule_bank, row_num, 1): ws_cell(ws_rule_bank, row_num, 2) for row_num in
                           range(1, ws_rule_bank.max_row + 1) if ws_cell(ws_rule_bank, row_num, 1) is not None}

ls_col_all = [ws_cell(ws_rule_type, row_num, 2) for row_num in range(1, max_row(ws_rule_type) + 1)]

ls_core_city = [ws_cell(ws_rule_others, row_num, 3) for row_num in range(2, ws_rule_others.max_row + 1) if
                ws_cell(ws_rule_others, row_num, 3) is not None]
dict_country_currency = {ws_cell(ws_rule_others, row_num, 6): ws_cell(ws_rule_others, row_num, 7) for row_num in
                         range(2, ws_rule_others.max_row + 1) if ws_cell(ws_rule_others, row_num, 6) is not None}
dict_country_development = {ws_cell(ws_rule_others, row_num, 6): ws_cell(ws_rule_others, row_num, 8) for row_num in
                            range(2, ws_rule_others.max_row + 1) if ws_cell(ws_rule_others, row_num, 6) is not None}
dict_risk_type = {ws_cell(ws_rule_others, row_num, 4): ws_cell(ws_rule_others, row_num, 5) for row_num in
                  range(2, ws_rule_others.max_row + 1) if ws_cell(ws_rule_others, row_num, 4) is not None}

row_num = 2
lsa = [ws_cell(ws_rule_null, 1, col) for col in range(2, ws_rule_null.max_column+1) if ws_cell(ws_rule_null, 1, col) is not None and ws_cell(ws_rule_null, 2, col) == 1]
dict_rule_null = {ws_cell(ws_rule_null, row_num, 1): [ws_cell(ws_rule_null, 1, col) for col in range(2, ws_rule_null.max_column+1) if ws_cell(ws_rule_null, 1, col) is not None and ws_cell(ws_rule_null, row_num, col) == 1]
                  for row_num in range(2,ws_rule_null.max_row+1) if ws_cell(ws_rule_null, row_num, 1) is not None}
dict_rule_type = {ws_cell(ws_rule_type, row_num, 2): ws_cell(ws_rule_type, row_num, 3) for row_num in range(1, ws_rule_type.max_row+1) if ws_cell(ws_rule_type, row_num, 2) is not None}
dict_rule_valid = {ws_cell(ws_rule_valid, 1, col_num): [ws_cell(ws_rule_valid, row_num, col_num) for row_num in range(1, ws_rule_valid.max_row+1) if ws_cell(ws_rule_valid, row_num, col_num) is not None]
                   for col_num in range(1, ws_rule_valid.max_column+1) if ws_cell(ws_rule_valid, 1, col_num) is not None}
dict_rule_lower = {ws_cell(ws_rule_type, row_num, 2): ws_cell(ws_rule_type, row_num, 4) for row_num in range(1, ws_rule_type.max_row+1) if ws_cell(ws_rule_type, row_num, 4) is not None}
dict_rule_upper = {ws_cell(ws_rule_type, row_num, 2): ws_cell(ws_rule_type, row_num, 5) for row_num in range(1, ws_rule_type.max_row+1) if ws_cell(ws_rule_type, row_num, 5) is not None}
dict_rule_compare = {'发行银行核心一级资本充足率': '发行银行一级资本充足率', '发行银行一级资本充足率': '发行银行资本充足率', '发行保险公司核心偿付能力充足率': '发行保险公司综合偿付能力充足率'}
dict_rule = {'not_null': dict_rule_null, 'type': dict_rule_type, 'valid': dict_rule_valid, 'lower': dict_rule_lower, 'upper': dict_rule_upper, 'compare': dict_rule_compare}
ls_null_values = {'无', '-'}