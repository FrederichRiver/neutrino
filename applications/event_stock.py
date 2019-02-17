#!/usr/bin/python3

"""
Geschafen im Feb 17, 2019
Verfasst von Friederich Fluss
Version
v1.0.1, Feb 17, 2019, First released.
"""
__version__ = '1.0.1-dev'
from libstock_dev import *


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
            self.get_stock_name(code)
        for code, name in y.code.items():
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


class downloadStockData(StockEventBase):
    def get_stock_list(self):
        index_list = self.finance.select_values('stock_index', 'stock_code')
        return index_list
    '''
    generate url
    read url
    download data
    resolve data
    push into pool
    write data in pool into database.
    '''


if __name__ == '__main__':
    # for stock in x:
    #    del_stock(stock, serv)

