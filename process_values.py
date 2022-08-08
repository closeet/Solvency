'''处理各种在数据库连接中的字段变换'''


def str_lize(string):
    if string is not None:
        return str(string)


def asset_id(product_name, product_id, com_asset_name=None, com_asset_id=None, account=None):
    try:
        ls_id = [str_lize(account)]

        if product_id == com_asset_id or product_name == com_asset_name:  # 标记豁免为自持
            com_asset_id = None
            com_asset_name = None
        if com_asset_name is None:  # 自持资产
            ls_id.append('自持')
            # print(ls_id)
            if product_id is None:  # 非标
                ls_id.append(str_lize(product_name))
                # print(ls_id)
            else:  # 标
                ls_id.append(str_lize(product_id))
                # print(ls_id)
        else:  # 穿透
            if com_asset_id is None:
                ls_id.append(str_lize(com_asset_name))
                # print(ls_id)
            else:
                ls_id.append(str_lize(com_asset_id))
                # print(ls_id)
            if product_id is None:  # 非标
                # print(2.1)
                ls_id.append(str_lize(product_name))
                # print(ls_id)
            else:  # 标
                ls_id.append(str_lize(product_id))
                # print(ls_id)
        # print(ls_id)
        # print('-'.join(ls_id))
        return '-'.join(ls_id)
    except:
        print(ls_id)


def ws_cell(ws, row_num, col_num):
    return ws.cell(row=row_num, column=col_num).value


def sql_value_lize(list_sql):
    ls_sql = []
    for items in list_sql:
        if items is None:
            ls_sql.append('null')
        else:
            ls_sql.append("'{}'".format(items))
    return ', '.join(ls_sql)


def sql_field_lize(list_sql):
    ls_sql = []
    for items in list_sql:
        ls_sql.append("`{}`".format(items))
    return ', '.join(ls_sql)


def max_row(ws):
    for row_max_row in range(2, ws.max_row + 2):
        if ws.cell(row=row_max_row, column=1).value is None and \
                ws.cell(row=row_max_row+1, column=1).value is None and \
                ws.cell(row=row_max_row+2, column=1).value is None and \
                ws.cell(row=row_max_row+3, column=1).value is None and \
                ws.cell(row=row_max_row+4, column=1).value is None :
            data_raw_max_row = row_max_row - 1
            break
    return data_raw_max_row


def cut_list(lists, cut_len):
    res_data = []
    if len(lists) > cut_len:
        for i in range(int(len(lists)/cut_len)):
            cut_a = lists[cut_len*i: cut_len*(i+1)]
            res_data.append(cut_a)
        last_data = lists[int(len(lists)/cut_len)*cut_len:]
        if last_data:
            res_data.append(last_data)
    else:
        res_data.append(lists)
    return res_data
