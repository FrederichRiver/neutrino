#!/usr/bin/python3

"""
Geschafen im Feb 17, 2019
Version
v1.0.1-dev, Feb 17, 2019, First released.
v1.0.2-beta, Feb 18, 2019, Now can download stock data and record into
database.
"""
__version__ = '1.0.3-beta'
__author__ = 'Friederich Fluss'
import time
import pandas as pd
import chardet
import requests
from common.libbase import *
from mysql.libmysql8_dev import MySQLBase
from finance.libstock_dev import StockEventBase
url = 'http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_Shibor_Data_{0}.xls&downLoadPath=data&nameOld=1{0}.xls&shiborSrc=http://www.shibor.org/shibor/'


class EventStockPrice(StockEventBase):
    def run(self, code, field):
        prices = self.stock.select_values(code, field)
        df = pd.DataFrame(list(prices), columns=field.split(','))
        return df

class EventRecordStock(StockEventBase):
    """
    a pool managed by the class
    if not full continue download and fill the pool
    if full, hang the line and wait until space.
    a data recorder write data to databases.
    First in First out.
    """

    def run(self):
        stock_list = create_stock_list()
        newlist = self.stock_filter(stock_list)
        for code in newlist:
            print(code)
            self.get_stock_name(code)
        for code, name in y.code.items():
            print(code, name)
            self.record_stock(code, name)

    def stock_filter(self, stock_list):
        index_list = self.finance.select_values('stock_index', 'stock_code')
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
        url_ne_index = readurl('URL_NE_INDEX')
        query_index = neteaseindex(code)
        netease_stock_index_url = url_ne_index.format(query_index, self.today)
        try:
            result = opencsv(netease_stock_index_url, 'gb18030')
            if len(result) > 0:
                #print(code, result.iloc[1,2])
                stock_name = result.iloc[1, 2].replace(' ', '')
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


class EventDownloadStockData(StockEventBase):
    def __init__(self):
        super(EventDownloadStockData, self).__init__()
        self.url = 'test'

    def get_stock_list(self):
        index_list = self.finance.select_values(
            'stock_index', 'stock_code')
        return index_list

    def get_url(self):
        self.url = readurl('url_ne_stock')

    def ne_index(self, index: str) -> str:
        if index[0:2] == 'SH':
            return index.replace('SH', '0')
        elif index[0:2] == 'SZ':
            return index.replace('SZ', '1')
        else:
            return None

    def download(self, code):
        start_time = self.start_time(code)
        end_time = self.today.replace('-', '')
        t = self.ne_index(code)
        url = self.url.format(t, start_time, end_time)
        print(url)
        result = opencsv(url, 'gb18030')
        return result

    def start_time(self, code):
        t = self.finance.select_values('stock_index', 'gmt_modified', "stock_code ='{0}'".format(code))
        if t:
            if t[0][0]:
                result = t[0][0].strftime('%Y%m%d')
            else:
                result = '19901219'
        else:
                result = '19901219'
        return result
    def run(self):
        self.get_url()
        stock_list = self.get_stock_list()
        for stock in stock_list:
            print(stock[0])
            data = self.download(stock[0])
            if len(data):
                data.replace('None', 0.0)
                self.analysis(data, stock[0])

    def analysis(self, data, code):
        data.replace('None', 0.0)

        for i in range(0, data.shape[0])[::-1]:
            if self.stock.select_values(
                    code, '*',
                    "trade_date='%s'" % data.iloc[i, 0]) == ():
                try:
                    columns = 'trade_date,close_price,\
                            high_price,low_price,\
                            open_price,gestern_preis,\
                            amplitude,volume,value'
                    content = "'{0}','{1}','{2}','{3}',\
                            '{4}','{5}','{6}','{7}',\
                            '{8}'".format(data.iloc[i, 0],
                                          data.iloc[i, 3], data.iloc[i, 4],
                                          data.iloc[i, 5], data.iloc[i, 6],
                                          data.iloc[i, 7], data.iloc[i, 9],
                                          data.iloc[i, 10], data.iloc[i, 11])
                    self.stock.insert_value(code, columns, content)
                except Exception as e:
                    err('Inserting err when fetching stocks: %s' % e)
            else:
                try:
                    columns = 'close_price,\
                            high_price,low_price,\
                            open_price,gestern_preis,\
                            amplitude,volume,value'
                    content = "'{0}','{1}','{2}','{3}',\
                            '{4}','{5}','{6}','{7}'".format(
                        data.iloc[i, 3], data.iloc[i, 4],
                        data.iloc[i, 5], data.iloc[i, 6],
                        data.iloc[i, 7], data.iloc[i, 9],
                        data.iloc[i, 10], data.iloc[i, 11])
                    self.stock.update_table(code, content,
                                            "trade_date='%s'" % data.iloc[i, 0])
                except Exception as e:
                    err('Updating error when fetching stocks: %s' % e)
            self.finance.update_table(
                'stock_index',
                "gmt_modified='%s'" % data.iloc[i, 0],
                "stock_code='%s'" % code)


class EventRecordShibor(StockEventBase):
    def __init__(self):
        super(EventRecordShibor, self).__init__()
        self.shibor = MySQLBase('root', '6414939', 'bank')

    def run(self):
        year_list = range(2006, 2019)
        for year in year_list:
            url_new = url.format(year)
            req = requests.get(url_new)
            result = pd.read_excel(url_new)
            #print(result.iloc[1,0].strftime('%Y-%m-%d'))
            self.record_shibor(result)

    def record_shibor(self, df):
        for i in range(0, df.shape[0])[::-1]:
            dt = df.iloc[i, 0].strftime('%Y-%m-%d')
            if self.shibor.select_values('shibor',
                '*', "release_date='%s'" % dt) == ():
                try:
                    columns = 'release_date, overnight,\
                    1W,2W,1M,3M,6M,9M,1Y'
                    content = "'{0}','{1}','{2}','{3}','{4}',\
                    '{5}','{6}','{7}','{8}'"
                    content = content.format(
                            dt, df.iloc[i, 1],
                            df.iloc[i, 2], df.iloc[i, 3],
                            df.iloc[i, 4], df.iloc[i, 5],
                            df.iloc[i, 6], df.iloc[i, 7],
                            df.iloc[i, 8])
                    self.shibor.insert_value('shibor',
                            columns, content)
                except Exception as e:
                    err('Inserting err when fetching shibor: %s' % e)
            else:
                try:
                    columns = 'overnight,1W,2W,1M,3M,6M,9M,1Y'
                    content = "'{0}','{1}','{2}','{3}','{4}',\
                            '{5}','{6}','{7}'"
                    content = content.format(df.iloc[i, 1],
                            df.iloc[i, 2], df.iloc[i, 3],
                            df.iloc[i, 4], df.iloc[i, 5],
                            df.iloc[i, 6], df.iloc[i, 7],
                            df.iloc[i, 8])
                except Exception as e:
                    err('Updateing err when fetching shibor: %s'% e)

if __name__ == '__main__':
    #time.sleep(3)
    print('start!')
    #y = EventRecordStock()
    #y.run()
    x = EventDownloadStockData()
    x.get_url()
    #x.start_time('SH600072')
    x.run()
    #shibor = EventRecordShibor()
    #shibor.run()
