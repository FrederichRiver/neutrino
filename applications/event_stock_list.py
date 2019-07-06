#!/usr/bin/python3

from libmysql8 import *
from utils import readurl, neteaseindex,opencsv,err,today 
import time
_version__ = '1.0.2-beta'


def get_stock_name(code):
    url_ne_index = readurl('URL_163_MONEY')
    query_index = neteaseindex(code)
    netease_stock_index_url = url_ne_index.format(query_index,
            '19901219',today())
    print(netease_stock_index_url)
    try:
        result = opencsv(netease_stock_index_url, 'gb18030')
        if len(result) > 0:
            print(code, result.iloc[1,2])
            stock_name = result.iloc[1, 2].replace(' ', '')
            self.code[code] = stock_name
    except Exception as e:
        err('Seaching index error: %s' % e)
        time.sleep(10)


if __name__ == '__main__':
    """
    test = MySQLBase('root', '6414939', 'test')
    result = test.session.query(formStockList)
    print(result)
    for st in result:
        print(st.stock_code)
    """
    result = get_stock_name('SH600001')
    print(result)
