#!/usr/bin/python3
# event_stock

from libmysql8 import MySQLBase
from utils import readurl, neteaseindex, opencsv, recordBase, today
from datetime import datetime
from libstock import create_stock_list
import logging
import time
from form import formStockList 

_version__ = '1.0.2-beta'



def event_record_stock():
    stock_engine = MySQLBase('root', '6414939', 'stock')
    stock_list = create_stock_list(flag='all')
    for stock in stock_list:
        _record_stock(stock, stock_engine.session)

def _get_file(code):
    url_ne_index = readurl('URL_163_MONEY')
    query_index = neteaseindex(code)
    netease_stock_index_url = url_ne_index.format(query_index,
            '19901219',
            today())
    return opencsv(netease_stock_index_url, 'gb18030')

def _get_stock_name(code):
    try:
        result = _get_file(code)
        if len(result) > 0:
            stock_name = result.iloc[1, 2].replace(' ', '')
            return code, stock_name
    except Exception as e:
        recordBase('Seaching index error: %s' % e, level=logging.ERROR)
        time.sleep(10)
        return code, ""


def _record_stock(stock, session):
    try:
        result = session.query(formStockList).filter_by(
            stock_code=stock).first()
        if result is None:
            code, name = _get_stock_name(stock)
            print(f"{code}: {name}")
            stk = formStockList(stock_code=code,
                                stock_name=name,
                                gmt_create=datetime.today())
            session.add(stk)
            session.commit()
    except Exception as e:
        recordBase(e, level=logging.INFO)


def event_download_stock_data():
    stock_engine = MySQLBase('root', '6414939', 'stock')
    result = stock_engine.session.query(formStockList.stock_code).all()
    for x in result:
        print(x[0])
        # download_stock_data
        _download_stock_data(x[0])


def _download_stock_data(stock_code):
    result = _get_file(stock_code)
    print(result)


if __name__ == '__main__':
    test = MySQLBase('root', '6414939', 'test')
    # event_record_stock()
    # event_download_stock_data()
    stock_engine = MySQLBase('root', '6414939', 'test')
    result = _get_file('SH600001')
    print(result.head(5))
    result.drop(['股票代码'],axis=1,inplace=True)
    print(result.head(4))
    result.to_sql(name='SH600001',
            con=test.engine,
            if_exists='append',
            index=False,
            index_label=False)
    
