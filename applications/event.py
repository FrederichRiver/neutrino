#!/usr/bin/python3
# event_stock

from libmysql8 import mysqlHeader
from libstock import (
    create_stock_list,
    EventTradeDataManager,
    EventCreateInterestTable,
    EventRecordInterest,
    EventFlag,
    EventTradeDetail,
    EventFinanceReport)
from libstock import EventRehabilitation
from dev import fetch_finance_info, fetch_cooperation_info
import time

__version__ = '1.0.12'


def event_init_stock():
    """
    Init database from a blank stock list.
    """
    header = mysqlHeader('stock', 'stock2020', 'stock')
    event = EventTradeDataManager()
    event._init_database(header)
    stock_list = create_stock_list()
    for stock in stock_list:
        event.record_stock(stock)


def event_record_stock():
    header = mysqlHeader('stock', 'stock2020', 'stock')
    event = EventTradeDataManager()
    event._init_database(header)
    event.security_list = event.fetch_all_security_list()
    for stock in event.security_list:
        event.record_stock(stock)


def event_download_stock_data():
    header = mysqlHeader('stock', 'stock2020', 'stock')
    event = EventTradeDataManager()
    event._init_database(header)
    result = self.mysql.session.query(
            formStockList.stock_code).all()
    # result format:
    # (stock_code,)
    for stock in result:
        print(f"{time.ctime()}: Download {stock[0]} stock data.")
        event.download_stock_data(stock[0])


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
        # event.update_balance_sheet(stock)
        event.update_income_statement(stock)


def event_download_trade_detail_data():
    header = mysqlHeader('root', '6414939', 'test')
    trade_date_list = ["20191129"]
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


def event_cooperation_info():
    header = mysqlHeader('root', '6414939', 'test')
    event = StockEventBase()
    event._init_database(header)
    stock_list = event.fetch_all_stock_list()
    # stock_list = ['SH601818']
    for stock in stock_list:
        print("fetch cooperation: ", stock)
        try:
            fetch_cooperation_info(stock)
        except Exception as e:
            print(e)


def event_finance_info():
    header = mysqlHeader('root', '6414939', 'test')
    event = StockEventBase()
    event._init_database(header)
    stock_list = event.fetch_all_stock_list()
    # stock_list = ['SH601818']
    for stock in stock_list:
        print("fetch finance: ", stock)
        try:
            fetch_finance_info(stock)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    header = mysqlHeader('stock', 'stock2020', 'stock')
    event_init_stock()
    # event_download_stock_data()
    # event_create_interest_table()
    # event_flag_stock()
    # event_record_interest()
    # event_download_trade_detail_data()
    # event_download_finance_report()
    # event_record_stock(header)
