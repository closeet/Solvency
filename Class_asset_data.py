import openpyxl
import os
from datetime import datetime
from static_parameters import *
from process_values import *
# from dynamic_parameters import *



"""读取后序列化"""
ls_core_city = []
dict_developed_market = {}
dict_type_capital_type = {}
dict_exchange = {}


def check_not_null(data):
    if data is None:
        return 1
    else:
        return 0


def check_null(data):
    if data is not None:
        return 2
    else:
        return 0


def check_type(data, data_type):
    if data is not None:
        if data_type == 'int':
            if isinstance(data, int) or isinstance(data, float):
                return 0
            else:
                return 3
        else:
            if isinstance(data, eval(data_type)):
                return 0
            else:
                return 3


def check_value(data, ls_valid):
    if data is not None:
        if data not in ls_valid:
            return 4
        else:
            return 0


def check_compare_number(data1, data2):
    if data1 is not None and isinstance(data1, str) == 0 and data2 is not None and isinstance(data2, str) == 0:
        if data1 > data2:
            return 5
        else:
            return 0


def check_l_limit(data, limit):
    if data is not None and isinstance(data, str) == 0:
        if data < limit:
            return 6
        else:
            return 0


def check_u_limit(data, limit):
    if data is not None and isinstance(data, str) == 0:
        if data > limit:
            return 7
        else:
            return 0


def data_check_process(check, dict_problem, cols):
    global bull_data_check
    dict_problem[cols] = check
    bull_data_check = check


def clean_null(data_type):
    if data_type == 'int' or data_type == 'float':
        return 0
    if data_type == 'str':
        return '未提供数据'
    if data_type == 'datetime':
        global evaluate_year, evaluate_month, evaluate_day
        return datetime(evaluate_year, evaluate_month, evaluate_day)


def clean_null_value(data_type):
    if data_type == 'int' or data_type == 'float':
        return 0
    if data_type == 'datetime':
        global evaluate_year, evaluate_month, evaluate_day
        return datetime(evaluate_year, evaluate_month, evaluate_day)


def clean_type(data, data_type):
    if data_type == 'int' or data_type == 'float':
        if isinstance(data, str) and data.find(',')+1:
            data = ''.join(data.split(','))
        return float(data)
    if data_type == 'str':
        return str(data)
    if data_type == 'datetime':
        return datetime(data)


class AssetData:
    def __init__(self, dict_data: dict):
        self.value = list(dict_data.values())
        self.col = list(dict_data.keys())
        self.data = dict_data
        self.data_raw = dict(zip(self.col, self.value))
        self.value_not_null = [values for values in list(dict_data.values()) if values is not None]
        self.col_not_null = [list(dict_data.keys())[i] for i, j in enumerate(list(dict_data.values())) if j is not None]
        self.data_not_null = zip(self.col_not_null, self.value_not_null)
        self.asset_type = self.data['资产类型']


    def data_check(self):
        global dict_rule
        dict_data_rule = dict_rule
        dict_problem = {}
        bull_data_check = 0
        if check_not_null(self.data['资产类型']):
            dict_problem['资产类型'] = check_null(self.data['资产类型'])
        else:
            asset_type = self.asset_type
            for cols_check in self.data.keys():
                data_check = self.data[cols_check]
                if cols_check in dict_data_rule['not_null'][asset_type] and check_not_null(data_check):
                    data_check_process(check_not_null(data_check), dict_problem, cols_check)
                if check_type(data_check, dict_data_rule['type'][cols_check]) and bull_data_check == 0:
                    data_check_process(check_type(data_check, dict_data_rule['type'][cols_check]), dict_problem, cols_check)
                if cols_check in dict_data_rule['valid'].keys() and bull_data_check == 0 \
                        and check_value(data_check, dict_data_rule['valid'][cols_check]):
                    data_check_process(check_value(data_check, dict_data_rule['valid'][cols_check]), dict_problem, cols_check)
                if cols_check in dict_data_rule['upper'].keys() and bull_data_check == 0 and data_check is not None\
                        and check_u_limit(data_check, dict_data_rule['upper'][cols_check]):
                    data_check_process(check_u_limit(data_check, dict_data_rule['valid'][cols_check]), dict_problem, cols_check)
                if cols_check in dict_data_rule['lower'].keys() and bull_data_check == 0 and data_check is not None\
                        and check_l_limit(data_check, dict_data_rule['lower'][cols_check]):
                    data_check_process(check_l_limit(data_check, dict_data_rule['valid'][cols_check]), dict_problem, cols_check)
                if cols_check in dict_data_rule['compare'].keys() and bull_data_check == 0 and data_check is not None\
                        and check_compare_number(data_check, self.data[dict_data_rule['compare'][cols_check]]):
                    data_check_process(
                        check_compare_number(data_check, self.data[dict_data_rule['compare'][cols_check]]), dict_problem, cols_check)
                    dict_problem[dict_data_rule['compare'][cols_check]] = \
                        check_compare_number(data_check, self.data[dict_data_rule['compare'][cols_check]])
        return dict_problem

    @property
    def cleansed_data(self):
        global ls_null_values, dict_rule
        dict_data_rule = dict_rule
        data_to_clean = {}
        data_to_clean.update(self.data)
        for col_clean in data_to_clean.keys():
            if data_to_clean[col_clean] in ls_null_values:
                data_to_clean[col_clean] = clean_null_value(dict_data_rule['type'][col_clean])
        for col_problem in self.data_check().keys():
            if self.data_check()[col_problem] == 1:
                data_to_clean[col_problem] = clean_null(dict_data_rule['type'][col_problem])
            if self.data_check()[col_problem] == 3:
                data_to_clean[col_problem] = clean_type(data_to_clean[col_problem], dict_data_rule['type'][col_problem])
        # data_to_clean['资产识别'] = self.asset_id
        return data_to_clean

    @property
    def sd_data(self):
        sd_data = {'资产识别': self.asset_id}
        sd_data.update(self.cleansed_data)
        return sd_data

    @property
    def labeled_data(self):
        labeled_data = {'穿透情况': self.penetration_type, '是否穿透': self.penetration,
                        '基础/非基础--底层': self.basic_after_penetration, '基础/非基础--表层': self.basic_after_penetration,
                        '境内外': self.foreign_invest, '资产分类--表层': self.asset_type_surface,
                        '资产大类--表层': self.asset_general_type_surface, '资产广类--表层': self.asset_type_more_general_surface,
                        '资产广类': self.asset_type_more_general}
        labeled_data.update(self.sd_data)
        return labeled_data

    @property
    def asset_id(self):
        return asset_id(self.data['资产简称'], self.data['产品代码'], self.data['表层资产简称'], self.data['表层资产产品代码'],
                        self.data['账户'])

    @property
    def penetration_type(self):
        if self.data['表层资产简称'] is not None and self.data['资产简称'] == self.data['表层资产简称']:
            return '豁免'
        elif self.data['表层资产简称'] is not None:
            return '穿透'
        elif self.data['表层资产简称'] is None:
            return '自持'
        else:
            print('穿透标识有误')

    @property
    def penetration(self):
        if self.penetration_type == '穿透':
            return '穿透'
        elif self.penetration_type in ['豁免', '自持']:
            return '未穿透'
        else:
            print('穿透情况有误')

    @property
    def foreign_invest(self):
        if self.data['所在国家（地区）'] is not None:
            return '境外'
        else:
            return '境内'

    @property
    def basic_after_penetration(self):
        if self.asset_type in ls_penetration_exempt_type:
            return '底层为非基础资产'
        else:
            return '底层为基础资产'

    @property
    def basic_before_penetration(self):
        if self.data['表层资产简称'] is not None:
            return '表层非基础资产'
        else:
            return '表层基础资产'

    @property
    def asset_type_surface(self):
        if self.basic_before_penetration == '表层非基础资产':
            return self.data['表层资产类型']
        else:
            return self.asset_type

    @property
    def asset_general_type_surface(self):
        if self.basic_before_penetration == '表层非基础资产':
            return self.data['表层资产大类']
        else:
            return self.data['资产大类']

    @property
    def asset_type_more_general(self):
        return dict_type_general[self.data['资产大类']]

    @property
    def asset_type_more_general_surface(self):
        if self.basic_before_penetration == '表层非基础资产':
            return dict_type_general[self.data['表层资产大类']]
        else:
            return dict_type_general[self.data['资产大类']]


