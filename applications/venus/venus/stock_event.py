#!/usr/bin/python3


__version__ = '1.2.15'
__all__ = [
    'event_record_new_stock', 'event_download_stock_data',
    'event_download_index_data', 'event_flag_quit_stock',
    'event_init_interest', 'event_record_interest',
    'event_flag_stock', 'event_flag_b_stock',
    'event_flag_index', 'event_rehabilitation',
    'event_record_cooperation_info', 'event_finance_info',
    'event_init_stock', 'event_download_finance_report',
    'event_update_shibor', 'event_download_trade_detail_data',
    'event_get_hk_list', 'event_record_orgid',
    'event_download_balance_data', 'event_download_cashflow_data',
    'event_download_income_data'
    ]

# Event Trade Data Manager


def event_init_stock():
    """
    Init database from a blank stock list.
    """
    from dev_global.env import GLOBAL_HEADER
    from venus.stock_manager import EventTradeDataManager
    event = EventTradeDataManager(GLOBAL_HEADER)
    stock_list = create_stock_list()
    for stock in stock_list:
        event.record_stock(stock)


def event_record_new_stock():
    from dev_global.env import GLOBAL_HEADER
    from venus.stock_base import StockList
    from venus.stock_manager import EventTradeDataManager
    sl = StockList()
    event = EventTradeDataManager(GLOBAL_HEADER)
    stock_list = sl.get_stock()
    for stock_code in stock_list:
        event.record_stock(stock_code)
        # event.init_stock_data(stock_code)


def event_download_stock_data():
    from dev_global.env import GLOBAL_HEADER
    from venus.stock_manager import EventTradeDataManager
    event = EventTradeDataManager(GLOBAL_HEADER)
    stock_list = event.get_all_stock_list()
    for stock_code in stock_list:
        event.download_stock_data(stock_code)


def event_download_index_data():
    from dev_global.env import GLOBAL_HEADER
    from venus.stock_manager import EventTradeDataManager
    event = EventTradeDataManager(GLOBAL_HEADER)
    stock_list = event.get_all_index_list()
    for stock_code in stock_list:
        event.download_stock_data(stock_code)


# delete, not use.
def event_create_interest_table():
    pass


def event_flag_quit_stock():
    from dev_global.env import GLOBAL_HEADER
    from venus.stock_flag import EventStockFlag
    event = EventStockFlag(GLOBAL_HEADER)
    stock_list = event.get_all_stock_list()
    # stock_code = 'SH601818'
    for stock_code in stock_list:
        flag = event.flag_quit_stock(stock_code)
        if flag:
            flag = 'q'
        else:
            flag = 't'
        sql = (
            f"UPDATE stock_manager set flag='{flag}' "
            f"WHERE stock_code='{stock_code}'")
        event.mysql.engine.execute(sql)


# event record interest
def event_init_interest():
    import time
    import numpy as np
    from dev_global.env import GLOBAL_HEADER
    from venus.stock_interest import EventInterest
    from jupiter.utils import ERROR
    event = EventInterest(GLOBAL_HEADER)
    event.get_all_stock_list()
    for stock_code in event.stock_list:
        # stock code format: SH600000
        try:
            tab = event.resolve_interest_table(stock_code)
            if not tab.empty:
                tab.replace(['--'], np.nan, inplace=True)
                tab = event.data_clean(tab)
                event.batch_insert_interest_to_sql(tab)
        except Exception as e:
            ERROR(e)
            ERROR(f"Error while initializing interest of {stock_code}")


def event_record_interest():
    """
    Insert interest line by line.
    """
    pass


def event_flag_stock():
    import re
    from dev_global.env import GLOBAL_HEADER
    from venus.stock_flag import EventStockFlag
    event = EventStockFlag(GLOBAL_HEADER)
    stock_list = event.get_all_security_list()
    for stock_code in stock_list:
        if re.match(r'^SH60|^SZ00|^SZ300', stock_code):
            event.flag_stock(stock_code)


def event_flag_b_stock():
    import re
    from dev_global.env import GLOBAL_HEADER
    from venus.stock_flag import EventStockFlag
    event = EventStockFlag(GLOBAL_HEADER)
    stock_list = event.get_all_security_list()
    for stock_code in stock_list:
        if re.match(r'^SH900|^SZ200', stock_code):
            event.flag_b_stock(stock_code)


def event_flag_index():
    import re
    from dev_global.env import GLOBAL_HEADER
    from venus.stock_flag import EventStockFlag
    event = EventStockFlag(GLOBAL_HEADER)
    stock_list = event.get_all_security_list()
    for stock_code in stock_list:
        if re.match(r'^SH000|^SH950|^SZ399', stock_code):
            event.flag_index(stock_code)


def event_rehabilitation():
    pass


def event_record_cooperation_info():
    from dev_global.env import GLOBAL_HEADER
    from venus.company import EventCompany
    from jupiter.utils import ERROR, INFO
    event = EventCompany(GLOBAL_HEADER)
    stock_list = event.get_all_stock_list()
    # stock_list = ['SH601818']
    for stock_code in stock_list:
        try:
            event.get_cooperation_info(stock_code)
        except Exception as e:
            ERROR("Error occours while recording company infomation.")
            ERROR(e)


def event_finance_info():
    pass


def event_download_finance_report():
    from dev_global.env import GLOBAL_HEADER
    from venus.finance_report import EventFinanceReport
    event = EventFinanceReport(GLOBAL_HEADER)
    stock_list = event.get_all_stock_list()
    for stock in stock_list:
        print(f"Download finance report of {stock}.")
        # event.update_balance_sheet(stock)
        event.update_income_statement(stock)
        event.update_balance_sheet(stock)
        event.update_cashflow_sheet(stock)


def event_update_shibor():
    import pandas
    from dev_global.env import GLOBAL_HEADER
    from venus.shibor import EventShibor
    event = EventShibor(GLOBAL_HEADER)
    year_list = range(2006, pandas.Timestamp.today().year + 1)
    for year in year_list:
        url = event.get_shibor_url(year)
        df = event.get_excel_object(url)
        event.get_shibor_data(df)


def event_download_trade_detail_data():
    from dev_global.env import GLOBAL_HEADER
    from polaris.mysql8 import mysqlHeader
    from venus.stock_manager import EventTradeDataManager
    import datetime
    from jupiter.utils import ERROR
    event = EventTradeDataManager(GLOBAL_HEADER)
    today = datetime.date.today()
    trade_date_list = [
        (today - datetime.timedelta(days=i)).strftime('%Y%m%d') for i in range(1, 6)
    ]
    stock_list = event.get_all_stock_list()
    for trade_date in trade_date_list:
        for stock in stock_list:
            # print(f"Download detail trade data {stock}: {trade_date}")
            try:
                event.get_trade_detail_data(stock, trade_date)
            except Exception as e:
                ERROR(e)


def event_get_hk_list():
    from dev_global.env import GLOBAL_HEADER
    from venus.cninfo import cninfoSpider
    event = cninfoSpider(GLOBAL_HEADER)
    df = event.get_hk_stock_list()
    event._insert_stock_manager(df)


def event_record_orgid():
    from dev_global.env import GLOBAL_HEADER
    from venus.cninfo import cninfoSpider
    event = cninfoSpider(GLOBAL_HEADER)
    df = event.get_stock_list()
    event._update_stock_manager(df)
    df = event.get_hk_stock_list()
    event._update_stock_manager(df)


def event_download_balance_data():
    from dev_global.env import GLOBAL_HEADER
    from jupiter.utils import ERROR
    from venus.finance_report import EventFinanceReport
    event = EventFinanceReport(GLOBAL_HEADER)
    stock_list = event.get_all_stock_list()
    for stock_code in stock_list:
        try:
            event.update_balance(stock_code)
        except Exception as e:
            ERROR(f"Error occours while recording {stock_code} balance sheet.")

def event_download_cashflow_data():
    from dev_global.env import GLOBAL_HEADER
    from jupiter.utils import ERROR
    from venus.finance_report import EventFinanceReport
    event = EventFinanceReport(GLOBAL_HEADER)
    stock_list = event.get_all_stock_list()
    for stock_code in stock_list:
        try:
            event.update_cashflow(stock_code)
        except Exception as e:
            ERROR(f"Error occours while recording {stock_code} cashflow sheet.")
            ERROR(e)

def event_download_income_data():
    from dev_global.env import GLOBAL_HEADER
    from jupiter.utils import ERROR
    from venus.finance_report import EventFinanceReport
    event = EventFinanceReport(GLOBAL_HEADER)
    stock_list = event.get_all_stock_list()
    for stock_code in stock_list:
        try:
            event.update_income(stock_code)
        except Exception as e:
            ERROR(f"Error occours while recording {stock_code} income sheet.")
            ERROR(e)


if __name__ == "__main__":
    # event_download_finance_report()
    # event_download_stock_data()
    # event_record_new_stock()
    # event_flag_quit_stock()
    # event_flag_index()
    # event_record_cooperation_info()
    # event_update_shibor()
    # event_init_interest()
    # event_download_trade_detail_data()
    from dev_global.env import GLOBAL_HEADER
    from jupiter.utils import ERROR
    from venus.finance_report import EventFinanceReport
    event = EventFinanceReport(GLOBAL_HEADER)
    stock_list = event.get_all_stock_list()
    for stock_code in stock_list:
        try:
            event.update_income(stock_code)
            event.update_balance(stock_code)
            event.update_cashflow(stock_code)
        except Exception as e:
            ERROR(f"Error occours while recording {stock_code} income sheet.")
            ERROR(e)