from Class_asset_data import AssetData
from dynamic_parameters import *
from static_parameters import *

ls_bond = ['政策性金融债券', '商业银行债券', '非银行金融债券', '银行发行的二级资本工具', '其他保险公司发行的次级债、资本补充债券',
           '企业债', '公司债', '短期融资券、超短期融资券', '中期票据', '政府支持机构债券', '同业存单', '信贷资产支持证券',
           '资产支持票据', '证券交易所挂票交易的资产支持证券', '国债', '地方政府债']
ls_bond_risk_free = ['国债', '地方政府债']
ls_bond_low_risk = ['政策性金融债券', '政府支持机构债券']
ls_bond_spreads = [bond for bond in ls_bond if bond not in ls_bond_risk_free and bond not in ls_bond_low_risk]
ls_green_bond = [bond for bond in ls_bond if bond not in ls_bond_low_risk]


class MinCapital(AssetData):
    @property
    def rf0(self):
        asset_type = self.asset_type
        dur = self.labeled_data['修正久期']
        rating = self.labeled_data['信用评级']
        bank_type = self.labeled_data['存款银行类型']
        bank_adequacy = self.labeled_data['银行资本充足率']
        account_age = self.labeled_data['账龄']

        """
        默认股指期货合约价值小于套保的股票价值，后续进行修正，对股指期货和套保股票的价值判断系数
        没有对境外固收、权益做出区分 仅适用境外上市股票 境外长股投
        不想写再保分出了 有点复杂 有空再说

        """

        if asset_type == '沪深主板股':
            return 0.35
        elif asset_type == '创业板股' \
                or self.labeled_data['资产类型'] == '科创板股':
            return 0.45
        elif asset_type == '未上市股权':
            return 0.41
        elif asset_type == '对子公司的长股投' or asset_type == '对子公司的境外长股投':
            if self.labeled_data['投资对象性质'] == '保险类子公司' or self.labeled_data['投资对象性质'] == '属于保险主业范围的子公司':
                return 0.35
            else:
                return 1
        elif asset_type == '合营企业、联营企业的长股投' or asset_type == '合营企业、联营企业的境外长股投':
            if self.labeled_data['是否在公开市场交易'] == '是':
                return 0.35
            else:
                return 0.41
        elif asset_type == '债券基金':
            return 0.06
        elif asset_type == '股票基金':
            return 0.28
        elif asset_type == '混合基金' or asset_type == '商品及金融衍生品基金':
            return 0.23
        elif asset_type == '货币市场基金':
            return 0.01
        elif asset_type == '可转债' or asset_type == '可交换债':
            return 0.23
        elif asset_type == '股指期货空头合约':
            if self.labeled_data['是否满足会计准则规定的套期有效性要求'] == '是':
                if self.labeled_data['套期期限'] >= 1:
                    return -0.35
                else:
                    return 0
            else:
                return 0.35
        elif asset_type == '股指期货多头合约':
            return 0.35
        elif asset_type == '优先股' or asset_type == '无固定期限资本债券':
            if self.labeled_data['是否带有强制转换为普通股或减记条款'] == '是':
                if self.labeled_data['发行机构类型'] == '非金融机构':
                    return 0.25
                elif self.labeled_data['发行机构类型'] == '银行':
                    if self.labeled_data['发行银行资本充足率'] < 0.08 \
                            or self.labeled_data['发行银行一级资本充足率'] < 0.06 \
                            or self.labeled_data['发行银行核心一级资本充足率'] < 0.05:
                        return 0.45
                    else:
                        if self.labeled_data['发行银行类型'] == '政策性银行' or self.labeled_data['发行银行类型'] == '国有大型商业银行':
                            return 0.15
                        elif self.labeled_data['发行银行类型'] == '股份制商业银行':
                            return 0.2
                        elif self.labeled_data['发行银行类型'] == '城市商业银行':
                            return 0.25
                        else:
                            return 0.3
                elif self.labeled_data['发行机构类型'] == '保险':
                    if self.labeled_data['发行保险公司综合偿付能力充足率'] < 1 \
                            or self.labeled_data['发行保险公司核心偿付能力充足率'] < 0.5:
                        return 0.45
                    else:
                        return 0.15
                elif self.labeled_data['发行机构类型'] == '资产管理公司':
                    if self.labeled_data['发行银行资本充足率'] < 0.125 \
                            or self.labeled_data['发行银行一级资本充足率'] < 0.1 \
                            or self.labeled_data['发行银行核心一级资本充足率'] < 0.09:
                        return 0.45
                    else:
                        return 0.2
                else:
                    pass
            else:
                if self.labeled_data['发行机构类型'] == '非金融机构':
                    return 0.1
                else:
                    return 0.15
        elif asset_type == '投资性不动产物权' \
                or asset_type == '不动产项目公司股权' \
                or asset_type == '向控股的经营投资性房地产业务的项目公司提供的各项融资借款':
            return 0.15
        elif asset_type == '境外权益类资产（其他权益类资产）':
            return 0.39
        elif asset_type == '政策性金融债券':
            if dur > 5:
                return dur * 0.001 + 0.025
            elif 0 <= dur <= 5:
                return dur * (dur * -0.0012 + 0.012)
            else:
                pass
        elif asset_type == '政府支持机构债券':
            if dur > 5:
                return dur * 0.001 + 0.03
            elif 0 <= dur <= 5:
                return dur * (-0.001 * dur + 0.012)
            else:
                pass
        elif asset_type in ls_bond_spreads:
            if rating == 'AAA':
                if dur > 5:
                    return dur * 0.015
                elif 0 <= dur <= 5:
                    return dur * (dur * 0.0006 + 0.012)
                else:
                    pass
            elif rating == 'AA+':
                if dur > 5:
                    return dur * 0.02
                elif 0 <= dur <= 5:
                    return dur * (dur * 0.0007 + 0.0165)
                else:
                    pass
            elif rating == 'AA':
                if dur > 5:
                    return dur * 0.0295
                elif 0 <= dur <= 5:
                    return dur * (dur * 0.0009 + 0.025)
                else:
                    pass
            elif rating == 'AA-':
                if dur > 5:
                    return dur * 0.038
                elif 0 <= dur <= 5:
                    return dur * (dur * 0.001 + 0.033)
                else:
                    pass
            elif rating == 'A+':
                if dur > 5:
                    return dur * 0.05
                elif 0 <= dur <= 5:
                    return dur * (dur * 0.002 + 0.04)
                else:
                    pass
            elif rating == 'A':
                if dur > 5:
                    return dur * 0.06
                elif 0 <= dur <= 5:
                    return dur * (dur * 0.003 + 0.045)
                else:
                    pass
            elif rating == 'A-':
                if dur > 5:
                    return dur * 0.07
                elif 0 <= dur <= 5:
                    return dur * (dur * 0.004 + 0.05)
                else:
                    pass
            elif rating == 'BBB+':
                if dur > 5:
                    return dur * 0.075
                elif 0 <= dur <= 5:
                    return dur * (dur * 0.005 + 0.05)
                else:
                    pass
            else:
                if dur > 5:
                    return dur * 0.1
                elif 0 <= dur <= 5:
                    return dur * (dur * 0.01 + 0.05)
                else:
                    pass
        elif asset_type == '拆出资金':
            return 0.03
        elif asset_type == '存放在第三方支付机构账户的资金':
            return 0.05
        elif asset_type == '定期存款' or asset_type == '协议存款' or asset_type == '大额存单':
            if bank_type == '国有大型商业银行' or bank_type == '政策性银行':
                return 0.005
            elif bank_type == '股份制商业银行':
                if bank_adequacy >= 0.12:
                    return 0.03
                elif bank_adequacy < 0.12:
                    return 0.05
                else:
                    pass
            elif bank_type == '城市商业银行':
                if bank_adequacy >= 0.135:
                    return 0.04
                elif 0.125 <= bank_adequacy < 0.135:
                    return 0.08
                elif 0.12 <= bank_adequacy < 0.125:
                    return 0.1
                elif bank_adequacy <= 0.12:
                    return 0.15
                else:
                    pass
            elif bank_type == '农村商业银行':
                if bank_adequacy >= 0.145:
                    return 0.08
                elif 0.135 <= bank_adequacy < 0.145:
                    return 0.1
                elif 0.125 <= bank_adequacy < 0.135:
                    return 0.15
                elif bank_adequacy <= 0.125:
                    return 0.18
                else:
                    pass
            else:
                if bank_adequacy >= 0.135:
                    return 0.1
                elif bank_adequacy < 0.135:
                    return 0.18
                else:
                    pass
        elif asset_type == '保本结构性存款':
            if bank_type == '国有大型商业银行' or bank_type == '政策性银行':
                return 0.055
            elif bank_type == '股份制商业银行':
                if bank_adequacy >= 0.12:
                    return 0.08
                elif bank_adequacy < 0.12:
                    return 0.1
                else:
                    pass
            elif bank_type == '城市商业银行':
                if bank_adequacy >= 0.135:
                    return 0.10
                elif 0.125 <= bank_adequacy < 0.135:
                    return 0.13
                elif 0.12 <= bank_adequacy < 0.125:
                    return 0.15
                elif bank_adequacy <= 0.12:
                    return 0.20
                else:
                    pass
            elif bank_type == '农村商业银行':
                if bank_adequacy >= 0.145:
                    return 0.13
                elif 0.135 <= bank_adequacy < 0.145:
                    return 0.15
                elif 0.125 <= bank_adequacy < 0.135:
                    return 0.20
                elif bank_adequacy <= 0.125:
                    return 0.23
                else:
                    pass
            else:
                if bank_adequacy >= 0.135:
                    return 0.15
                elif bank_adequacy < 0.135:
                    return 0.23
                else:
                    pass
        elif asset_type == '非保本结构性存款' or asset_type == '未通过重大保险风险测试的保险业务所对应的应收及预付款':
            return 0.5
        elif asset_type == '应收保费':
            if self.labeled_data['是否是享受各级政府保费补贴的业务'] == '是':
                if account_age == '不大于9个月':
                    return 0
                elif account_age == '(6个月，12个月]':
                    return 0.2
                elif account_age == '(12个月，18个月]':
                    return 0.7
                elif account_age == '18个月以上':
                    return 1
                else:
                    pass
            else:
                if account_age == '不大于6个月':
                    return 0
                elif account_age == '(6个月，12个月]':
                    return 0.5
                elif account_age == '(12个月，18个月]' or account_age == '18个月以上':
                    return 1
                else:
                    pass
        elif asset_type == '预付赔款' or asset_type == '待抵扣预交税费':
            return 0
        elif asset_type == '除上述外的其他应收及预付款':
            if account_age == '不大于6个月':
                return 0.03
            elif account_age == '(6个月，12个月]':
                return 0.15
            elif account_age == '(12个月，18个月]':
                return 0.5
            elif account_age == '18个月以上':
                return 1
            else:
                pass
        elif asset_type == '其他底层贷款资产' or asset_type == '保险公司向集团外的关联方提供的融资借款' \
                or asset_type == '保险公司向其非控股的、经营投资性房地产业务的项目公司的各项融资借款':
            if self.labeled_data['资产风险分类等级'] == '正常类':
                return 0.085
            elif self.labeled_data['资产风险分类等级'] == '关注类':
                return 0.135
            elif self.labeled_data['资产风险分类等级'] == '次级类':
                return 0.3
            elif self.labeled_data['资产风险分类等级'] == '可疑类':
                return 0.5
            elif self.labeled_data['资产风险分类等级'] == '损失类':
                return 1
            else:
                pass
        elif asset_type == '债务担保':
            return 0.3
        elif asset_type == '保单质押贷款':
            return 0.05
        elif asset_type == '国债' or asset_type == '地方政府债':
            return 0
        else:
            return 0

    @property
    def k1(self):
        global dict_k1
        if self.asset_type in ['沪深主板股', '创业板股', '科创板股'] and self.penetration_type == '自持':
            return dict_k1['涨跌幅']
        elif self.asset_type in ['投资性不动产物权', '不动产项目公司股权', '向控股的经营投资性房地产业务的项目公司提供的各项融资借款'] \
                and self.labeled_data['所在城市'] not in ls_core_city:
            return dict_k1['地区']
        elif self.asset_type == ['境外权益类资产（其他权益类资产）'] and self.labeled_data['所在国家（地区）'] in ls_country_developing:
            return dict_k1['市场类型']
        elif self.asset_type in ls_green_bond and self.labeled_data['是否为支持碳减排项目的绿色债券'] == '是':
            return dict_k1['绿债']
        else:
            return 0

    @property
    def k2(self):
        if self.asset_type in ['沪深主板股', '创业板股', '科创板股', '境外权益类资产（其他权益类资产）'] \
                and self.labeled_data['是否为沪深300成分股'] == '是':
            return -0.05
        else:
            return 0

    @property
    def k_concentration_counter_party(self):
        global ls_counter_party
        if self.labeled_data['交易对手'] in ls_counter_party:
            return 0.4
        else:
            return 0

    @property
    def k_concentration_asset_type(self):
        global ls_asset_type
        if self.labeled_data['资产五大类分类'] in ls_asset_type:
            return 0.2
        else:
            return 0

    @property
    def k_layer(self):
        if self.labeled_data['交易层级'] is not None:
            if self.labeled_data['表层资产类型'] in ['固定收益类信托计划', '债权投资计划', '资产支持计划']:
                return (self.labeled_data['交易层级'] - 1) * 0.1
            else:
                return self.labeled_data['交易层级'] * 0.1
        else:
            return 0

    @property
    def k_sum(self):
        return 1 + self.k1 + self.k2 + self.k_concentration_counter_party + self.k_concentration_asset_type + self.k_layer

    @property
    def minimum_capital(self):
        if self.asset_type == '股指期货空头':
            return self.labeled_data['认可价值'] * self.rf0 * self.labeled_data['套期有效性']
        else:
            return self.labeled_data['认可价值'] * self.rf0 * self.k_sum

    @property
    def minimum_capital_type(self):
        return dict_risk_type[self.asset_type]

    @property
    def interest_minimum_capital(self):
        if self.labeled_data['应收利息'] is not None:
            if self.minimum_capital_type == '利差':
                if self.labeled_data['信用评级'] == 'AAA' or self.asset_type in ls_bond_low_risk:
                    rf_interest = 0.006
                elif self.labeled_data['信用评级'] in ['AA+', 'AA', 'AA-']:
                    rf_interest = 0.015
                elif self.labeled_data['信用评级'] in ['A+', 'A', 'A-']:
                    rf_interest = 0.025
                else:
                    rf_interest = 0.03
            elif self.minimum_capital_type == '违约':
                rf_interest = self.rf0
            else:
                rf_interest = 0
            return rf_interest * self.k_sum * self.labeled_data['应收利息']
        else:
            return 0

    @property
    def surface_minimum_capital(self):
        if self.labeled_data['表层资产类型'] in ['债权投资计划', '资产支持计划', '固定收益类信托计划']:
            if self.labeled_data['表层资产信用评级'] == 'AAA':
                rf_surface = 0.01
            elif self.labeled_data['表层资产信用评级'] == 'AA+':
                rf_surface = 0.015
            elif self.labeled_data['表层资产信用评级'] == 'AA':
                rf_surface = 0.020
            elif self.labeled_data['表层资产信用评级'] == 'AA-':
                rf_surface = 0.025
            elif self.labeled_data['表层资产信用评级'] in ['A+', 'A', 'A-']:
                rf_surface = 0.075
            else:
                rf_surface = 0.15
            if self.labeled_data['表层资产类型'] == '债权投资计划':
                k_surface = -0.2
            else:
                k_surface = 0
            return self.labeled_data['表层资产认可价值'] * rf_surface * (1 + k_surface)
        else:
            return 0

    @property
    def exchange_minimum_capital(self):
        if self.labeled_data['所在国家（地区）'] is not None:
            if dict_country_currency[self.labeled_data['所在国家（地区）']] == '美元':
                rf_exchange = 0.05
            elif dict_country_currency[self.labeled_data['所在国家（地区）']] in ['欧元', '英镑']:
                rf_exchange = 0.08
            elif dict_country_currency[self.labeled_data['所在国家（地区）']] == '其他货币':
                rf_exchange = 0.15
            else:
                pass
            return rf_exchange * self.k_sum * self.labeled_data['认可价值']
        else:
            return 0

    @property
    def total_min_cap(self):
        return self.minimum_capital + self.interest_minimum_capital + self.surface_minimum_capital + self.exchange_minimum_capital

    @property
    def counter_party_min_cap(self):
        return (self.k_concentration_counter_party / self.k_sum) * self.minimum_capital

    @property
    def asset_type_min_cap(self):
        return (self.k_concentration_asset_type / self.k_sum) * self.minimum_capital

    @property
    def calc_data(self):
        calc_data = {'RF0': self.rf0, 'K1': self.k1, 'K2': self.k2, 'K交易对手': self.k_concentration_counter_party,
                     'K大类资产': self.k_concentration_asset_type, 'K交易层级': self.k_layer, '调整因子': self.k_sum,
                     '最低资本': self.minimum_capital, '最低资本类型': self.minimum_capital_type,
                     '应收利息最低资本': self.interest_minimum_capital, '表层资产最低资本': self.surface_minimum_capital,
                     '汇率最低资本': self.exchange_minimum_capital, '最低资本和': self.total_min_cap,
                     '交易对手最低资本': self.counter_party_min_cap, '大类资产最低资本': self.asset_type_min_cap
                     }
        calc_data.update(self.labeled_data)
        return calc_data
