import openpyxl
import pyxlsb
wb_insurance = pyxlsb.open_workbook('负债端数据/2022负债评估结果6月.xlsb')
ws = wb_insurance.get_sheet('202206')
ls_data=[]
for index, row in enumerate(ws.rows()):
    ls_row = []
    if index > 3:
        for col in [2, 3, 18, 20, 19, 7, 34, 23, 24, 25, 26, 27, 28, 29, 37, 38, 30, 31, 32, 33, 35]:
            ls_row.append(row[col].v)
        ls_row[0] = str(ls_row[0]).split('.')[0]
        ls_data.append(ls_row)
ls_ul = []
ls_trad = []
for index_row, ls_ in enumerate(ls_data):
    if ls_[0][-1] == '3':
        if ls_ul == []:
            ls_ul = ls_[2:]
        else:
            for index_col, col_ in enumerate(ls_):
                if index_col > 1:
                    if ls_ul[index_col-2] is None:
                        ls_ul[index_col-2] = 0
                    if col_ is None:
                        col_ = 0
                    ls_ul[index_col-2] += col_
    else:
        if ls_trad == []:
            ls_trad = ls_[2:]
        else:
            for index_col, col_ in enumerate(ls_):
                if index_col > 1:
                    if ls_trad[index_col-2] is None:
                        ls_trad[index_col-2] = 0
                    if col_ is None:
                        col_ = 0
                    ls_trad[index_col-2] += col_
wb_model = openpyxl.load_workbook('偿付能力汇总模型.xlsx')
ws_liab = wb_model['二期负债及保险风险']
# for range()

