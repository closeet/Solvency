import time

if __name__ == '__main__':
    time_start_all = time.time()
    from data_to_SQL import data_to_sql
    data_to_sql()
    from calculation_to_sql import calc_to_sql
    calc_to_sql()
    time_end_all = time.time()
    print('共用时{}秒'.format(time_end_all - time_start_all))

