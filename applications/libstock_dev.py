#!/usr/bin/python3

"""
Geschafen im Feb 13, 2019
Verfasst von Friederich Fluss
Version
v1.1.4, Feb 13, 2019, rebuild this lib.
v1.2.5, Feb 17, 2019, build class stockeventbase, not perfect.
"""
from mysql.libmysql8_dev import MySQLBase
__version__ = '1.2.4-dev'
from libbase import *
from datetime import *
"""
Define the data format transfer between api is in fotmat below.

"""


def create_stock_list(flag='all'):
    indexs = []
    sha = ['SH600000']*4000
    for i in range(len(sha)):
        sha[i] = 'SH' + '60' + str(i).zfill(4)
    sza = ['SZ000001']*1000
    for i in range(len(sza)):
        sza[i] = 'SZ' + str(i).zfill(6)
    cyb = ['SZ300001']*1000
    for i in range(len(cyb)):
        cyb[i] = 'SZ' + '300' + str(i).zfill(3)
    zxb = ['SZ002000']*1000
    for i in range(len(zxb)):
        zxb[i] = 'SZ' + '002' + str(i).zfill(3)
    szb = ['SZ200001']*1000
    for i in range(len(szb)):
        szb[i] = 'SZ' + '200' + str(i).zfill(3)
    shi = ['SH000000']*2000
    for i in range(999):
        shi[i] = 'SH' + str(i).zfill(6)
        shi[i + 1000] = 'SH' + '950' + str(i).zfill(3)
    szi = ['SZ399000']*1000
    for i in range(len(szi)):
        szi[i] = 'SZ' + '399' + str(i).zfill(3)
    hk = ['HK00001']*10000
    for i in range(len(hk)):
        hk[i] = 'HK'+str(i+1).zfill(5)

    if flag == 'all':
        indexs.extend(sha)
        indexs.extend(sza)
        indexs.extend(cyb)
        indexs.extend(zxb)
        indexs.extend(szb)
        indexs.extend(shi)
        indexs.extend(szi)
    elif flag == 'stocks':
        indexs.extend(sha)
        indexs.extend(sza)
    elif flag == 'a':
        indexs.extend(sha)
        indexs.extend(sza)
    elif flag == 'b':
        indexs.extend(shb)
        indexs.extend(szb)
    elif flag == 'zxb':
        indexs.extend(zxb)
    elif flag == 'cyb':
        indexs.extend(cyb)
    elif flag == 'hk':
        indexs.extend(hk)
    else:
        pass
    return indexs


def del_stock(stock_code, serv):
    ms = MySQLBase(serv[0], serv[1], serv[2])
    ms.drop_table(stock_code)
    ms.remove_data('finance.stock_index',
                   "stock_code='{0}'".format(stock_code))
    return 1

class StockEventBase(object):
    def __init__(self):
        self.queue = []
        self.code = {}
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.finance = MySQLBase('root', '6414939', 'finance')
        self.stock = MySQLBase('root', '6414939', 'stock_data')
class EventRecordStock(StockEventBase): 
    """
    a pool managed by the class
    if not full continue download and fill the pool
    if full, hang the line and wait until space.
    a data recorder write data to databases.
    First in First out.
    """
    def stop(self):
        pass
    def pause(self):
        pass
    def main_event(self, task):
        pass

    def run(self, stock_list):
        for code in stock_list:
            self.get_stock_name(code)

    def stock_filter(self, stock_list):
        index_list = self.finance.select_values('stock_index','stock_code')
        old_list = []
        for index in index_list:
            if self.finance.table_exists(index[0]):
                old_list.append(index[0])
        new_list = []
        for index in stock_list:
            if index not in old_list:
                new_list.append(index)
        return new_list

    def get_stock_name(self, code):
        url_ne_index =readurl('URL_NE_INDEX')
        query_index = neteaseindex(code)
        netease_stock_index_url = url_ne_index.format(query_index, self.today)
        try:
            result = opencsv(netease_stock_index_url, 'gb18030')
            if len(result) >0:
                #print(code, result.iloc[1,2])
                stock_name = result.iloc[1,2].replace(' ','')
                self.code[code] = stock_name
        except Exception as e:
            err('Seaching index error: %s' % e)
            time.sleep(10)

    def record_stock(self, code, name):
        '''create table SHxxx if exists'''
        content = databasedef('def_stock') 
        self.stock.create_table(code, content)
        ''' update stock index'''
        column = 'stock_code, stock_name, gmt_create'
        value = "'{0}','{1}','{2}'".format(code, name, self.today)
        self.finance.insert_value('stock_index', column, value)

def sql_record_stock():
    pass

if __name__ == '__main__':
    print(datetime.now().strftime('%Y-%m-%d'))

    x = create_stock_list()
    serv = ('root', '6414939', 'stock_data')
    #for stock in x:
    #    del_stock(stock, serv)
    y = EventRecordStock()
    newlist = y.stock_filter(x)
    for code in newlist[:10]:
        y.get_stock_name(code)
    print(y.code)
    for code,name in y.code.items():
        y.record_stock(code,name)
