import openpyxl
from numpy import matrix
from math import sqrt

wb_report = openpyxl.load_workbook('偿付能力汇总模型0630_0708V3.xlsx', data_only=True)
ws_s01 = wb_report['S01-偿付能力状况表']
ls_problem = []


def cell(ws, row, col):
    cell_value = ws.cell(row=row, column=col).value
    if cell_value is None:
        cell_value = 0
    elif type(cell_value) not in [eval('int'), eval('float')]:
        cell_value = float(cell_value)
    else:
        pass
    return cell_value


def check_equation(eq: bool, problem_description: str):
    if eq:
        pass
    else:
        ls_problem.append(problem_description)


mat_risk = matrix([[1, 0.2, 0.3, 0.15],
                   [0.2, 1, 0.1, 0.1],
                   [0.3, 0.1, 1, 0.35],
                   [0.15, 0.1, 0.35, 1]])

bool_ac_cap1 = bool(cell(ws_s01, 5, 3) - cell(ws_s01, 6, 3) == cell(ws_s01, 7, 3))
problem_ac_cap1 = '实际资本不等于认可资产减认可负债'
bool_ac_cap2 = bool(cell(ws_s01, 8, 3) + cell(ws_s01, 9, 3) + cell(ws_s01, 10, 3) + cell(ws_s01, 11, 3) == cell(ws_s01, 7, 3))
problem_ac_cap2 = '实际资本不等于核心资本与附属资本之和'
ls_min_cap = matrix([cell(ws_s01, 14, 3), cell(ws_s01, 15, 3), cell(ws_s01, 16, 3), cell(ws_s01, 17, 3)])
bool_min_cap = sqrt(ls_min_cap * mat_risk * ls_min_cap.T)
problem_nim_cap = '最低资本不等于各类风险的积'
