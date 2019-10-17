#!/usr/bin/python3
# event_stock

from libmysql8 import mysqlHeader
from libstock import (EventCreateStockTable,
                      EventDownloadStockData,
                      EventCreateInterestTable,
                      EventRecordInterest,
                      EventFlag)
from libstock_dev import EventRehabilitation
__version__ = '1.0.5'


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
        event.main_flag(stock_code)


def event_rehabilitation():
    header = mysqlHeader('root', '6414939', 'test')
    event = EventRehabilitation()
    event._init_database(header)
    stock_list = event.fetch_all_stock_list()
    for stock in stock_list:
        event.rehabilitate(stock)

if __name__ == "__main__":
    # event_init_stock()
    # event_download_stock_data()
    # event_create_interest_table()
    # event_flag_stock()
    event_record_interest()
