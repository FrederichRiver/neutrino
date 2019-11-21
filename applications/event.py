#!/usr/bin/python3
# event_stock

from libmysql8 import mysqlHeader
from libstock import (
    EventTradeDataManager,
    EventCreateInterestTable,
    EventRecordInterest,
    EventFlag,
    EventTradeDetail)
from libstock import EventRehabilitation
from libfinance import EventFinanceReport
from dev import fetch_finance_info, fetch_cooperation_info
import time

__version__ = '1.0.9'


def event_init_stock():
    header = mysqlHeader('root', '6414939', 'test')
    event = EventTradeDataManager()
    event._init_database(header)
    stock_list = create_stock_list()
    for stock in stock_list:
        print(f"{time.ctime()}: Create table {stock}.")
        self.record_stock(stock)


def event_record_stock():
    header = mysqlHeader('root', '6414939', 'test')
    event = EventTradeDataManager()
    event._init_database(header)
    self.fetch_all_security_list()
    for stock in self.security_list:
        print(f"{time.ctime()}: Create table {stock}.")
        self.record_stock(stock)


def event_download_stock_data():
    header = mysqlHeader('root', '6414939', 'test')
    event = EventTradeDataManager()
    event._init_database(header)
    result = self.mysql.session.query(
            formStockList.stock_code).all()
    # result format:
    # (stock_code,)
    for stock in result:
        print(f"{time.ctime()}: Download {stock[0]} stock data.")
        self.download_stock_data(stock[0])


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
        print(f"Calculating adjust factor of {stock}")
        event.rehabilitate(stock)
        event.update_adjust_factor(stock)


def event_download_finance_report():
    header = mysqlHeader('root', '6414939', 'test')
    event = EventFinanceReport()
    event._init_database(header)
    stock_list = event.fetch_all_stock_list()
    for stock in stock_list:
        # print(stock[2:])
        print(f"Download finance report of {stock}.")
        event.update_balance_sheet_asset(stock)


def event_download_trade_detail_data():
    header = mysqlHeader('root', '6414939', 'test')
    trade_date_list = ["20191120"]
    event = EventTradeDetail()
    event._init_database(header)
    stock_list = event.fetch_all_stock_list()
    for trade_date in trade_date_list:
        for stock in stock_list:
            print(f"Download detail trade data {stock}: {trade_date}")
            try:
                event.fetch_trade_detail_data(stock, trade_date)
            except Exception:
                pass


if __name__ == "__main__":
    # event_init_stock()
    # event_download_stock_data()
    # event_create_interest_table()
    # event_flag_stock()
    # event_record_interest()
    event_download_trade_detail_data()
