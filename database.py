import pymysql
from numpy import array
from process_values import sql_value_lize, sql_field_lize, cut_list


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

    def insert(self, table_name, col_name, values):
        try:
            if len(array(values).shape) == 1:
                str_values = "({})".format(sql_value_lize(values))
                str_col_name = "({})".format(sql_field_lize(col_name))
                sql = """INSERT INTO `{0}` {1}
                 VALUES{2}""".format(table_name, str_col_name, str_values)
                cursor = self.db_session()
                cursor.execute(sql)
                self.db.commit()
            else:
                values_cut = cut_list(values, 800)
                for value in values_cut:
                    ls_values = []
                    for ls in value:
                        ls_values.append(("({})".format(sql_value_lize(ls))))
                    str_values = ', '.join(ls_values)
                    str_col_name = "({})".format(sql_field_lize(col_name))
                    sql = """INSERT INTO `{0}` {1}
                     VALUES{2}""".format(table_name, str_col_name, str_values)
                    cursor = self.db_session()
                    cursor.execute(sql)
                    self.db.commit()
        except Exception as ex:
            print("Insertion Error: {}".format(ex))
            self.db.rollback()
        finally:
            self.close()

    def sql_exec(self, sql_string):
        try:
            cursor = self.db_session()
            # print("EXECUTING: {0}".format(sql_string))
            cursor.execute(sql_string)
            self.db.commit()
        except Exception as ex:
            print("SQL Error executing {1}: \n{0}".format(ex, sql_string))
            self.db.rollback()
        finally:
            self.close()


evaluate_year = "2022"
# evaluate_month = input("评估时点月份：")
evaluate_month = '6'
if evaluate_month in ['1', '3', '5', '7', '8', '10', '12']:
    evaluate_day = '31'
elif evaluate_month in ['4', '6', '9', '11']:
    evaluate_day = '30'
elif evaluate_month == '2':
    if int(evaluate_year) % 4 == 0:
        evaluate_day = '29'
    else:
        evaluate_day = '28'
else:
    print("输入时点有误")
evaluate_date_str = evaluate_year + evaluate_month.rjust(2, '0') + evaluate_day
table_name_raw = evaluate_date_str + '偿付能力原始数据'
table_name_labeled = evaluate_date_str + '偿付能力分类数据'
table_name_calc = evaluate_date_str + '偿付能力最低资本数据'
table_name_asset = evaluate_date_str + '财报口径资产数据'
sql_drop_table_raw = '''DROP TABLE ''' + table_name_raw
sql_drop_table_labeled = '''DROP TABLE ''' + table_name_labeled
sql_drop_table_calc = '''DROP TABLE ''' + table_name_calc
sql_drop_table_asset = '''DROP TABLE ''' + table_name_asset
sql_delete_table_raw = '''DELETE FROM ''' + table_name_raw + ''' WHERE `id`>=0'''
sql_delete_table_labeled = '''DELETE FROM ''' + table_name_labeled + ''' WHERE `id`>=0'''
sql_delete_table_calc = '''DELETE FROM ''' + table_name_calc + ''' WHERE `id`>=0'''
sql_delete_table_asset = '''DROP TABLE ''' + table_name_asset

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

sql_create_table_asset = '''
CREATE TABLE `''' + table_name_asset + '''` (
  `id` int NOT NULL AUTO_INCREMENT,
  `资产简称` varchar(255) NOT NULL,
  `资产全称` varchar(255) NOT NULL,
  `资产大类` varchar(255) NOT NULL,
  `资产类型` varchar(255) NOT NULL,
  `认可价值` double NOT NULL,
  `应收利息` double DEFAULT NULL,
  `账户` varchar(255) NOT NULL,
  `资产五大类分类` varchar(255) NOT NULL,
  `认可资产分类-小` varchar(255) NOT NULL,
  `认可资产分类-大` varchar(255) NOT NULL,
  `境内外` varchar(255) NOT NULL,
  
  PRIMARY KEY (`id`)
)
'''