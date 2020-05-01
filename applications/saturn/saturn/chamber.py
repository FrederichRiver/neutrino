#!/usr/bin/python3

from venus.stock_base import StockEventBase
from dev_global.env import GLOBAL_HEADER
import pandas

def user_func():
    # in_file = '/home/friederich/Downloads/test.txt'
    in_file = '/home/fred/test.txt'
    stock_name_list = []
    event = StockEventBase(GLOBAL_HEADER)
    with open(in_file, 'r') as f:
        result = f.readline()
        while result:
            stock_name_list.append(result[:-1])
            result = f.readline()

    stock_code_list = []
    for stock_name in stock_name_list:
        # sql = f"SELECT stock_code from stock_manager WHERE stock_name='{stock_name}'"
        stock_code = event.mysql.condition_select('stock_manager', 'stock_code', f"stock_name='{stock_name}'")
        if not stock_code.empty:
            # print(stock_code.values[0][0])
            stock_code_list.append(stock_code.values[0][0])

    stock_table = pandas.DataFrame()
    for stock_code in stock_code_list:
        # result = event.mysql.condition_select(stock_code, 'trade_date, close_price')
        result = event.mysql.select_values(stock_code, 'trade_date, close_price')
        result.columns = ['trade_date', stock_code]
        result.set_index('trade_date', inplace=True)
        stock_table = pandas.concat([stock_table, result], axis=1)

    stock_table = stock_table.tail(50)
    # print(stock_table)
    stock_table.to_excel('/home/fred/data.xls')
    # with open('/home/fred/data.txt', 'w') as f:
    #    f.write(stock_table)