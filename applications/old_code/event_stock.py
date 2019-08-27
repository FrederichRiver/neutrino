#!/usr/bin/python3

"""
Geschafen im Feb 17, 2019
Version
v1.0.1-dev, Feb 17, 2019, First released.
v1.0.2-beta, Feb 18, 2019, Now can download stock data and record into
database.
"""
__version__ = '1.0.2-beta'
__author__ = 'Friederich Fluss'
from libstock_dev import *
import time


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
        start_time = '19901219'
        end_time = self.today.replace('-', '')
        t = self.ne_index(code)
        url = self.url.format(t, start_time, end_time)
        print(url)
        result = opencsv(url, 'gb18030')
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


if __name__ == '__main__':
    #time.sleep(3)
    print('start!')
    #y = EventRecordStock()
    #y.run()
    x = EventDownloadStockData()
    x.get_url()
    x.run()
