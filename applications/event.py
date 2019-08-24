#!/usr/bin/python3
# event_stock

import re
import pandas as pd
from libmysql8 import mysqlHeader, mysqlBase
from form import formStockList
from libstock import create_stock_list, _download_stock_data
from libstock import fetch_no_flag_stock, _record_stock
__version__ = '1.0.3-beta'
"""
event registance:
event_initial_database
event_record_stock
event_download_stock_data
"""


"""
events for database maintance
"""


def event_stock_flag():
    header = mysqlHeader('root', '6414939', 'stock')
    mysql = mysqlBase(header)
    stock_list = fetch_no_flag_stock()
    df = pd.DataFrame(stock_list, columns=['stock_code'])
    df['flag'] = None
    print(df.head(5))
    for i in range(df.shape[0]):
        if re.match(r'^SH0', df.loc[i, 'stock_code']):
            df.loc[i, 'flag'] = 'index'
            print(df.iloc[i].values)
            sql = f"update stock_list set flag=\
                   '{df.loc[i,'flag']}' where stock_code=\
                    '{df.loc[i,'stock_code']}'"
            mysql.session.execute(sql)
            mysql.session.commit()
        elif re.match(r'^SH6', df.loc[i, 'stock_code']):
            df.loc[i, 'flag'] = 'stock'
            sql = f"update stock_list set flag=\
                   '{df.loc[i,'flag']}' where stock_code=\
                    '{df.loc[i,'stock_code']}'"
            mysql.session.execute(sql)
            mysql.session.commit()
        elif re.match(r'^SZ0', df.loc[i, 'stock_code']):
            df.loc[i, 'flag'] = 'stock'
            sql = f"update stock_list set flag=\
                   '{df.loc[i,'flag']}' where stock_code=\
                    '{df.loc[i,'stock_code']}'"
            mysql.session.execute(sql)
            mysql.session.commit()
        elif re.match(r'^SZ3', df.loc[i, 'stock_code']):
            df.loc[i, 'flag'] = 'stock'
            sql = f"update stock_list set flag=\
                   '{df.loc[i,'flag']}' where stock_code=\
                    '{df.loc[i,'stock_code']}'"
            mysql.session.execute(sql)
            mysql.session.commit()


def event_record_stock():
    header = mysqlHeader('root', '6414939', 'stock')
    mysql = mysqlBase(header)
    stock_list = create_stock_list(flag='all')
    for stock in stock_list:
        _record_stock(stock, mysql)


def event_download_stock_data():
    header = mysqlHeader('root', '6414939', 'stock')
    mysql = mysqlBase(header)
    result = mysql.session.query(formStockList.stock_code).all()
    for x in result:
        print(x[0])
        # download_stock_data
        _download_stock_data(x[0], mysql)


if __name__ == "__main__":
    pass
