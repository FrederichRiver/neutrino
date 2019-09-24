#!/usr/bin/python3
# event_stock

from libmysql8 import mysqlHeader
from libstock import (EventCreateStockTable,
                      EventDownloadStockData,
                      EventCreateInterestTable,
                      EventRecordInterest,
                      EventFlag)
__version__ = '1.0.4'


def event_init_stock():
    header = mysqlHeader('root', '6414939', 'test')
    event = EventCreateStockTable()
    event._init_database(header)
    event.sub_init_stock_table()


def event_record_stock():
    header = mysqlHeader('root', '6414939', 'test')
    event = EventCreateStockTable()
    event._init_database(header)
    event.sub_create_stock_table()


def event_download_stock_data():
    header = mysqlHeader('root', '6414939', 'test')
    event = EventDownloadStockData()
    event._init_database(header)
    event.download_stock_data()


def event_create_interest_table():
    header = mysqlHeader('root', '6414939', 'test')
    event = EventCreateInterestTable()
    event._init_database(header)
    event.create_interest_table()


def event_record_interest():
    header = mysqlHeader('root', '6414939', 'test')
    event = EventRecordInterest()
    event._init_database(header)
    event.record_interest()


def event_flag_stock():
    header = mysqlHeader('root', '6414939', 'test')
    event = EventFlag()
    event._init_database(header)
    event.fetch_all_security_list()
    for stock_code in event.security_list:
        event._flag_stock(stock_code)

if __name__ == "__main__":
    # event_init_stock()
    # event_download_stock_data()
    event_create_interest_table()
    # event_flag_stock()
