import pymysql
import sqlalchemy
import sqlalchemy.ext.declarative
import openpyxl
from numpy import array
from process_values import asset_id
from process_values import ws_cell
from process_values import sql_value_lize
from process_values import sql_field_lize, cut_list
from process_values import max_row



class MySqlConnection:
    def __init__(self, host=None, user=None, password=None, database=None, port=3306):

        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.db = self.connect_db()

    def connect_db(self):
        # try:
        db_connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                        port=self.port)
        return db_connection
        # except:
        #     self.db.ping(reconnect=True)

    def db_session(self):
        self.db = self.connect_db()
        cursor = self.db.cursor()
        return cursor

    def close(self):
        self.db.close()

    def sql_query(self, sql_query, num=None):
        try:
            cursor = self.db_session()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            if num is None:
                return result
            else:
                return result[:num]
        except Exception as ex:
            print("Query Error:{}".format(ex))
        finally:
            self.close

    def insert(self, table_name, col_name, values, ls_sql=None):
        try:
            if len(array(values).shape) == 1:
                str_values = "({})".format(sql_value_lize(values))
                str_col_name = "({})".format(sql_field_lize(col_name))
                sql = """INSERT INTO `{0}` {1}
                 VALUES{2}""".format(table_name, str_col_name, str_values)
                print(sql)
                # ls_sql.append(sql)
                cursor = self.db_session()
                cursor.execute(sql)
                self.db.commit()
            else:

                values_cut = cut_list(values, 800)
                for value in values_cut:
                    ls_values = []
                    for ls in value:
                        # print(ls)
                        # print(sql_value_lize(ls))
                        ls_values.append(("({})".format(sql_value_lize(ls))))
                        # print(ls_values)
                    str_values = ', '.join(ls_values)
                    str_col_name = "({})".format(sql_field_lize(col_name))
                    sql = """INSERT INTO `{0}` {1}
                     VALUES{2}""".format(table_name, str_col_name, str_values)
                    print(sql)
                    # ls_sql.append(sql)
                    cursor = self.db_session()
                    cursor.execute(sql)
                    self.db.commit()
        except Exception as ex:
            print("Insertion Error: {}".format(ex))
            self.db.rollback()
        finally:
            self.close()
            # return ls_sql

    def sql_exec(self, sql_string):
        try:
            cursor = self.db_session()
            print("EXECUTING: {0}".format(sql_string))
            cursor.execute(sql_string)
            self.db.commit()
        except Exception as ex:
            print("SQL Error executing {1}: \n{0}".format(ex, sql_string))
            self.db.rollback()
        finally:
            self.close()


evaluate_year = 2022
evaluate_month = 5
evaluate_day = 30
evaluate_date_str = str(evaluate_year) + str(evaluate_month).rjust(2, '0') + str(evaluate_day)
table_name_raw = evaluate_date_str + '偿付能力原始数据'
table_name_labeled = evaluate_date_str + '偿付能力分类数据'
table_name_calc = evaluate_date_str + '偿付能力最低资本数据'
sql_drop_table_raw = '''DROP TABLE ''' + table_name_raw
sql_drop_table_labeled = '''DROP TABLE ''' + table_name_labeled
sql_drop_table_calc = '''DROP TABLE ''' + table_name_calc
sql_delete_table_raw = '''DELETE FROM ''' + table_name_raw + ''' WHERE `id`>=0'''
sql_delete_table_labeled = '''DELETE FROM ''' + table_name_labeled + ''' WHERE `id`>=0'''
sql_delete_table_calc = '''DELETE FROM ''' + table_name_calc + ''' WHERE `id`>=0'''
sql_create_table_raw = '''
CREATE TABLE `''' + table_name_raw + '''` (
  `id` int NOT NULL AUTO_INCREMENT,
  `资产识别` varchar(255) NOT NULL,
  `资产简称` varchar(255) NOT NULL,
  `资产全称` varchar(255) NOT NULL,
  `资产大类` varchar(255) NOT NULL,
  `资产类型` varchar(255) NOT NULL,
  `产品代码` varchar(255) DEFAULT NULL,
  `交易对手` varchar(255) NOT NULL,
  `持有份数` double DEFAULT NULL,
  `购买成本` double NOT NULL,
  `认可价值` double NOT NULL,
  `应收利息` double DEFAULT NULL,
  `应收股利` double DEFAULT NULL,
  `账户` varchar(255) NOT NULL,
  `表层资产简称` varchar(255) DEFAULT NULL,
  `表层资产全称` varchar(255) DEFAULT NULL,
  `表层资产产品代码` varchar(255) DEFAULT NULL,
  `表层资产大类` varchar(255) DEFAULT NULL,
  `表层资产类型` varchar(255) DEFAULT NULL,
  `交易层级` int DEFAULT NULL,
  `表层资产交易对手` varchar(255) DEFAULT NULL,
  `表层资产购买成本` double DEFAULT NULL,
  `表层资产认可价值` double DEFAULT NULL,
  `表层资产应收利息` double DEFAULT NULL,
  `表层资产起息日` date DEFAULT NULL,
  `表层资产到期日` date DEFAULT NULL,
  `表层资产信用评级` varchar(255) DEFAULT NULL,
  `是否为沪深300成分股` varchar(255) DEFAULT NULL,
  `持股比例` double DEFAULT NULL,
  `是否带有强制转换为普通股或减记条款` varchar(255) DEFAULT NULL,
  `发行机构类型` varchar(255) DEFAULT NULL,
  `发行银行类型` varchar(255) DEFAULT NULL,
  `发行银行资本充足率` double DEFAULT NULL,
  `发行银行一级资本充足率` double DEFAULT NULL,
  `发行银行核心一级资本充足率` double DEFAULT NULL,
  `发行保险公司综合偿付能力充足率` double DEFAULT NULL,
  `发行保险公司核心偿付能力充足率` double DEFAULT NULL,
  `是否在公开市场交易` varchar(255) DEFAULT NULL,
  `投资对象性质` varchar(255) DEFAULT NULL,
  `减值前账面价值` double DEFAULT NULL,
  `套期保值组合` varchar(255) DEFAULT NULL,
  `是否满足会计准则规定的套期有效性要求` varchar(255) DEFAULT NULL,
  `套期有效性` double DEFAULT NULL,
  `套期期限` double DEFAULT NULL,
  `所在城市` varchar(255) DEFAULT NULL,
  `投资时间` date DEFAULT NULL,
  `计量属性` varchar(255) DEFAULT NULL,
  `账面价值` double DEFAULT NULL,
  `所在国家（地区）` varchar(255) DEFAULT NULL,
  `存款银行账户号` varchar(255) DEFAULT NULL,
  `存款银行类型` varchar(255) DEFAULT NULL,
  `银行资本充足率` double DEFAULT NULL,
  `剩余年限` double DEFAULT NULL,
  `信用评级` varchar(255) DEFAULT NULL,
  `修正久期` double DEFAULT NULL,
  `是否为支持碳减排项目的绿色债券` varchar(255) DEFAULT NULL,
  `资产风险分类等级` varchar(255) DEFAULT NULL,
  `再保分入人类型` varchar(255) DEFAULT NULL,
  `再保分入独立法人地区` varchar(255) DEFAULT NULL,
  `偿付能力` double DEFAULT NULL,
  `各级偿付能力是否达到监管要求` varchar(255) DEFAULT NULL,
  `再保公司评级` varchar(255) DEFAULT NULL,
  `有无担保措施` varchar(255) DEFAULT NULL,
  `地区是否获得偿付能力等效资格` varchar(255) DEFAULT NULL,
  `是否是享受各级政府保费补贴的业务` varchar(255) DEFAULT NULL,
  `账龄` varchar(255) DEFAULT NULL,
  `账户类别` varchar(255) DEFAULT NULL,
  `资产五大类分类` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
)
'''
sql_create_table_labeled = '''
CREATE TABLE `''' + table_name_labeled + '''` (
  `id` int NOT NULL AUTO_INCREMENT,
  `资产识别` varchar(255) NOT NULL,
  `资产简称` varchar(255) NOT NULL,
  `资产全称` varchar(255) NOT NULL,
  `资产大类` varchar(255) NOT NULL,
  `资产类型` varchar(255) NOT NULL,
  `产品代码` varchar(255) DEFAULT NULL,
  `交易对手` varchar(255) NOT NULL,
  `持有份数` double DEFAULT NULL,
  `购买成本` double NOT NULL,
  `认可价值` double NOT NULL,
  `应收利息` double DEFAULT NULL,
  `应收股利` double DEFAULT NULL,
  `账户` varchar(255) NOT NULL,
  `表层资产简称` varchar(255) DEFAULT NULL,
  `表层资产全称` varchar(255) DEFAULT NULL,
  `表层资产产品代码` varchar(255) DEFAULT NULL,
  `表层资产大类` varchar(255) DEFAULT NULL,
  `表层资产类型` varchar(255) DEFAULT NULL,
  `交易层级` int DEFAULT NULL,
  `表层资产交易对手` varchar(255) DEFAULT NULL,
  `表层资产购买成本` double DEFAULT NULL,
  `表层资产认可价值` double DEFAULT NULL,
  `表层资产应收利息` double DEFAULT NULL,
  `表层资产起息日` date DEFAULT NULL,
  `表层资产到期日` date DEFAULT NULL,
  `表层资产信用评级` varchar(255) DEFAULT NULL,
  `是否为沪深300成分股` varchar(255) DEFAULT NULL,
  `持股比例` double DEFAULT NULL,
  `是否带有强制转换为普通股或减记条款` varchar(255) DEFAULT NULL,
  `发行机构类型` varchar(255) DEFAULT NULL,
  `发行银行类型` varchar(255) DEFAULT NULL,
  `发行银行资本充足率` double DEFAULT NULL,
  `发行银行一级资本充足率` double DEFAULT NULL,
  `发行银行核心一级资本充足率` double DEFAULT NULL,
  `发行保险公司综合偿付能力充足率` double DEFAULT NULL,
  `发行保险公司核心偿付能力充足率` double DEFAULT NULL,
  `是否在公开市场交易` varchar(255) DEFAULT NULL,
  `投资对象性质` varchar(255) DEFAULT NULL,
  `减值前账面价值` double DEFAULT NULL,
  `套期保值组合` varchar(255) DEFAULT NULL,
  `是否满足会计准则规定的套期有效性要求` varchar(255) DEFAULT NULL,
  `套期有效性` double DEFAULT NULL,
  `套期期限` double DEFAULT NULL,
  `所在城市` varchar(255) DEFAULT NULL,
  `投资时间` date DEFAULT NULL,
  `计量属性` varchar(255) DEFAULT NULL,
  `账面价值` double DEFAULT NULL,
  `所在国家（地区）` varchar(255) DEFAULT NULL,
  `存款银行账户号` varchar(255) DEFAULT NULL,
  `存款银行类型` varchar(255) DEFAULT NULL,
  `银行资本充足率` double DEFAULT NULL,
  `剩余年限` double DEFAULT NULL,
  `信用评级` varchar(255) DEFAULT NULL,
  `修正久期` double DEFAULT NULL,
  `是否为支持碳减排项目的绿色债券` varchar(255) DEFAULT NULL,
  `资产风险分类等级` varchar(255) DEFAULT NULL,
  `再保分入人类型` varchar(255) DEFAULT NULL,
  `再保分入独立法人地区` varchar(255) DEFAULT NULL,
  `偿付能力` double DEFAULT NULL,
  `各级偿付能力是否达到监管要求` varchar(255) DEFAULT NULL,
  `再保公司评级` varchar(255) DEFAULT NULL,
  `有无担保措施` varchar(255) DEFAULT NULL,
  `地区是否获得偿付能力等效资格` varchar(255) DEFAULT NULL,
  `是否是享受各级政府保费补贴的业务` varchar(255) DEFAULT NULL,
  `账龄` varchar(255) DEFAULT NULL,
  `账户类别` varchar(255) DEFAULT NULL,
  `资产五大类分类` varchar(255) NOT NULL,
  `穿透情况` varchar(255) NOT NULL,
  `是否穿透` varchar(255) NOT NULL,
  `基础/非基础--底层` varchar(255) NOT NULL,
  `基础/非基础--表层` varchar(255) NOT NULL,
  `境内外` varchar(255) NOT NULL,
  `资产分类--表层` varchar(255) NOT NULL,
  `资产大类--表层` varchar(255) NOT NULL,
  `资产广类--表层` varchar(255) NOT NULL,
  `资产广类` varchar(255) NOT NULL,  
  PRIMARY KEY (`id`)
)
'''

sql_create_table_clac = '''
CREATE TABLE `''' + table_name_calc + '''` (
  `id` int NOT NULL AUTO_INCREMENT,
  `资产识别` varchar(255) NOT NULL,
  `资产简称` varchar(255) NOT NULL,
  `资产全称` varchar(255) NOT NULL,
  `资产大类` varchar(255) NOT NULL,
  `资产类型` varchar(255) NOT NULL,
  `产品代码` varchar(255) DEFAULT NULL,
  `交易对手` varchar(255) NOT NULL,
  `持有份数` double DEFAULT NULL,
  `购买成本` double NOT NULL,
  `认可价值` double NOT NULL,
  `应收利息` double DEFAULT NULL,
  `应收股利` double DEFAULT NULL,
  `账户` varchar(255) NOT NULL,
  `表层资产简称` varchar(255) DEFAULT NULL,
  `表层资产全称` varchar(255) DEFAULT NULL,
  `表层资产产品代码` varchar(255) DEFAULT NULL,
  `表层资产大类` varchar(255) DEFAULT NULL,
  `表层资产类型` varchar(255) DEFAULT NULL,
  `交易层级` int DEFAULT NULL,
  `表层资产交易对手` varchar(255) DEFAULT NULL,
  `表层资产购买成本` double DEFAULT NULL,
  `表层资产认可价值` double DEFAULT NULL,
  `表层资产应收利息` double DEFAULT NULL,
  `表层资产起息日` date DEFAULT NULL,
  `表层资产到期日` date DEFAULT NULL,
  `表层资产信用评级` varchar(255) DEFAULT NULL,
  `是否为沪深300成分股` varchar(255) DEFAULT NULL,
  `持股比例` double DEFAULT NULL,
  `是否带有强制转换为普通股或减记条款` varchar(255) DEFAULT NULL,
  `发行机构类型` varchar(255) DEFAULT NULL,
  `发行银行类型` varchar(255) DEFAULT NULL,
  `发行银行资本充足率` double DEFAULT NULL,
  `发行银行一级资本充足率` double DEFAULT NULL,
  `发行银行核心一级资本充足率` double DEFAULT NULL,
  `发行保险公司综合偿付能力充足率` double DEFAULT NULL,
  `发行保险公司核心偿付能力充足率` double DEFAULT NULL,
  `是否在公开市场交易` varchar(255) DEFAULT NULL,
  `投资对象性质` varchar(255) DEFAULT NULL,
  `减值前账面价值` double DEFAULT NULL,
  `套期保值组合` varchar(255) DEFAULT NULL,
  `是否满足会计准则规定的套期有效性要求` varchar(255) DEFAULT NULL,
  `套期有效性` double DEFAULT NULL,
  `套期期限` double DEFAULT NULL,
  `所在城市` varchar(255) DEFAULT NULL,
  `投资时间` date DEFAULT NULL,
  `计量属性` varchar(255) DEFAULT NULL,
  `账面价值` double DEFAULT NULL,
  `所在国家（地区）` varchar(255) DEFAULT NULL,
  `存款银行账户号` varchar(255) DEFAULT NULL,
  `存款银行类型` varchar(255) DEFAULT NULL,
  `银行资本充足率` double DEFAULT NULL,
  `剩余年限` double DEFAULT NULL,
  `信用评级` varchar(255) DEFAULT NULL,
  `修正久期` double DEFAULT NULL,
  `是否为支持碳减排项目的绿色债券` varchar(255) DEFAULT NULL,
  `资产风险分类等级` varchar(255) DEFAULT NULL,
  `再保分入人类型` varchar(255) DEFAULT NULL,
  `再保分入独立法人地区` varchar(255) DEFAULT NULL,
  `偿付能力` double DEFAULT NULL,
  `各级偿付能力是否达到监管要求` varchar(255) DEFAULT NULL,
  `再保公司评级` varchar(255) DEFAULT NULL,
  `有无担保措施` varchar(255) DEFAULT NULL,
  `地区是否获得偿付能力等效资格` varchar(255) DEFAULT NULL,
  `是否是享受各级政府保费补贴的业务` varchar(255) DEFAULT NULL,
  `账龄` varchar(255) DEFAULT NULL,
  `账户类别` varchar(255) DEFAULT NULL,
  `资产五大类分类` varchar(255) NOT NULL,
  `穿透情况` varchar(255) NOT NULL,
  `是否穿透` varchar(255) NOT NULL,
  `基础/非基础--底层` varchar(255) NOT NULL,
  `基础/非基础--表层` varchar(255) NOT NULL,
  `境内外` varchar(255) NOT NULL,
  `资产分类--表层` varchar(255) NOT NULL,
  `资产大类--表层` varchar(255) NOT NULL,
  `资产广类--表层` varchar(255) NOT NULL,
  `资产广类` varchar(255) NOT NULL,  
  `RF0` double DEFAULT NULL,  
  `K1` double DEFAULT NULL,
  `K2` double DEFAULT NULL,
  `K交易对手` double DEFAULT NULL,
  `K大类资产` double DEFAULT NULL,
  `K交易层级` double DEFAULT NULL,
  `调整因子` double DEFAULT NULL,
  `最低资本` double DEFAULT NULL,
  `最低资本类型` varchar(255) NOT NULL,
  `应收利息最低资本` double DEFAULT NULL,
  `表层资产最低资本` double DEFAULT NULL,
  `汇率最低资本` double DEFAULT NULL,
  `最低资本和` double DEFAULT NULL,
  `交易对手最低资本` double DEFAULT NULL,
  `大类资产最低资本` double DEFAULT NULL,
  
  PRIMARY KEY (`id`)
)
'''
#
# if __name__ == '__main__':
#     dict_table_col = {}
#     ls_col_name_data_raw = ["id", "资产识别", "资产简称", "资产全称", "资产大类", "资产类型", "产品代码", "交易对手", "持有份数", "购买成本",
#                             "认可价值", "应收利息", "应收股利", "账户", "表层资产简称", "表层资产全称", "表层资产产品代码", "表层资产大类",
#                             "表层资产类型", "交易层级", "表层资产交易对手", "表层资产购买成本", "表层资产认可价值", "表层资产应收利息",
#                             "表层资产起息日", "表层资产到期日", "表层资产信用评级", "是否为沪深300成分股", "持股比例",
#                             "是否带有强制转换为普通股或减记条款", "发行机构类型", "发行银行类型", "发行银行资本充足率", "发行银行一级资本充足率",
#                             "发行银行 核心一级 资本充足率", "发行保险公司综合偿付能力充足率", "发行保险公司核心偿付能力充足率", "是否在公开市场交易",
#                             "投资对象性质", "减值前账面价值", "套期保值组合", "是否满足会计准则规定的套期有效性要求", "套期有效性", "套期期限",
#                             "所在城市", "投资时间", "计量属性", "账面价值", "所在国家（地区）", "存款银行账户号", "存款银行类型",
#                             "银行资本充足率", "剩余年限", "信用评级", "修正久期", "是否为支持碳减排项目的绿色债券", "资产风险分类等级",
#                             "再保分入人类型", "再保分入独立法人地区", "偿付能力", "各级偿付能力是否达到监管要求", "再保公司评级", "有无担保措施",
#                             "地区是否获得偿付能力等效资格", "是否是享受各级政府保费补贴的业务", "账龄", "账户类别", "资产五大类分类"]
#     dict_table_col["data_raw"] = ls_col_name_data_raw
#
#     wb_value_data_raw = openpyxl.load_workbook('E:/和谐健康偿付能力数据库/数据/530汇总.xlsx')
#     ws_value_data_raw = wb_value_data_raw.worksheets[0]
#     ls_value_data_raw = []
#
#     ls_asset_id_para_col = [1, 5, 13, 15, 12]
#
#     # for row_num in range(2, max_row(ws_value_data_raw)):
#     #     ls_row = []
#     #     ls_asset_id_para = []
#     #     for cols in ls_asset_id_para_col:
#     #         ls_asset_id_para.append(ws_cell(ws_value_data_raw, row_num, cols))
#     #     for col_num in range(1, 67):
#     #         ls_row.append(ws_value_data_raw.cell(row=row_num, column=col_num).value)
#     #     ls_row.insert(0, asset_id(*ls_asset_id_para))
#     #     ls_value_data_raw.append(ls_row)
#     # print(ls_value_data_raw)
#     # sb_solv = MySqlConnection(host="localhost", user="root", password="19981027Phy", database="solvency_data")
#     sb_solv = MySqlConnection(host="localhost", user="root", password="19981027phy", database="solvency2")
#     sb_solv.connect_db()
#     sb_solv.insert("data_raw", ls_col_name_data_raw[1:], ls_value_data_raw)

# def insert_record


# engine = sqlalchemy.create_engine("mysql+pymysql://root:19981027phy@localhost:3306/solvency_data", echo=True)
# base = sqlalchemy.ext.declarative.declarative_base()
# class Asset(base):
#     __tablename__ = 'solvency_asset'
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
#     asset_id = sqlalchemy.Column(sqlalchemy.String(255), default=None, nullable=False, comment='资产识别')
#     asset_name_short = sqlalchemy.Column(sqlalchemy.String(255), default=None, nullable=False, comment='资产简称')
#     recognised_value = sqlalchemy.Column(sqlalchemy.Integer, default=None, nullable=False, comment='认可价值')
#
#     def __repr__(self):
#         a_id = self.asset_id
#         a_n_s = self.asset_name_short
#         r_v = self.recognised_value
#         return f"Asset:(asset_id={a_id}, asset_name_short={a_n_s}, recognised_value={r_v}"

# asset = Asset(asset_id="abc", ass)
