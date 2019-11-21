#!/usr/bin/python3
# from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import requests
from libmysql8 import mysqlHeader, mysqlBase, create_table_from_table
from libstock import wavelet_nr, StockEventBase, str2zero
from libstratagy import StratagyBase
from lxml import etree
from data_feature import ma
from form import formFinanceTemplate, formBalanceSheet

__version__ = '1.5.6-beta'


# ARIMA
def arima_test():
    header = mysqlHeader('root', '6414939', 'test')
    event = StockEventBase()
    event._init_database(header)

    series = d['close']
    model = ARIMA(series, order=(5, 1, 0))
    model_fit = model.fit(disp=0)
    print(model_fit.summary())


def segment():
    import numpy as np
    import matplotlib.pyplot as plt

    header = mysqlHeader('root', '6414939', 'test')
    event = StockEventBase()
    event._init_database(header)

    stock_code = 'SH601818'
    sql = f"SELECT close_price from {stock_code}"
    result = event.mysql.engine.execute(sql).fetchall()
    seg = []
    for data in result:
        seg.append(data[0])
    seg = seg[:50]
    seg = np.array(seg)
    seg_fil = wavelet_nr(seg)
    plt.plot(seg)
    plt.plot(seg_fil)
    plt.show()

# FFT
# SHIBOR
# 26EMA
# BullingBand
# VIX
# SHANGHAI
# US Dollar
# Gold
# Metal
# Oil


class stratagy_new(StratagyBase):
    def __init__(self):
        super(StratagyBase, self).__init__()

    def run(self):
        df = self.fetch_data('SH601818')
        df = ma(df, 5)
        df = ma(df, 10)
        df = df[-20:]
        print(df.head(5))


def fetch_html_table(url, attr=''):
    # get html table from url.
    # Return a string like table object.
    # attr: [@class='table_bg001 border_box limit_scale scr_table']
    content = requests.get(url, timeout=3)
    html = etree.HTML(content.text)
    table_list = html.xpath(f"//table{attr}")
    table = etree.tostring(table_list[0]).decode()
    return table


def table_2_dataframe():
    url = f"http://quotes.money.163.com/f10/zycwzb_{stock_code[2:]}.html#01c02"
    table = fetch_html_table(url, attr="[@class='table_bg001 border_box limit_sale scr_table']")
    t = pd.read_html(table)[0]
    result = t.T
    return result


def fetch_finance_info(stock_code):
    url = f"http://quotes.money.163.com/f10/zycwzb_{stock_code[2:]}.html#01c02"
    table = fetch_html_table(url, attr="[@class='table_bg001 border_box limit_sale scr_table']")
    t = pd.read_html(table)[0]
    result = t.T
    header = mysqlHeader('root', '6414939', 'test')
    mysql = mysqlBase(header)
    for index, row in result.iterrows():
        insert_sql = (
            "insert into finance_info (stock_code, report_date, eps, roe)"
            f"values ('{stock_code}','{index}',{str2zero(row[0])},{str2zero(row[18])})")
        update_sql = (
            f"update finance_info set eps={str2zero(row[0])}, roe={str2zero(row[18])} "
            f"where (stock_code='{stock_code}' and report_date='{index}')")
        try:
            mysql.engine.execute(sql)
        except Exception as e:
            mysql.engine.execute(update_sql)


def fetch_cooperation_info(stock_code):
    url = f"http://quotes.money.163.com/f10/gszl_{stock_code[2:]}.html#01f02"
    table = fetch_html_table(url, attr="[@class='table_bg001 border_box limit_sale table_details']")
    t = pd.read_html(table)[0]
    # print(t.iloc[12, 1])
    header = mysqlHeader('root', '6414939', 'test')
    mysql = mysqlBase(header)
    insert_sql = (
        "INSERT INTO cooperation_info ("
        "stock_code, short_name, name, english_name, legal_representative, address,"
        "chairman, secratery, main_business, business_scope, introduction)"
        "VALUES ( "
        f"'{stock_code}','{t.iloc[2, 1]}','{t.iloc[2, 1]}','{t.iloc[3, 1]}',"
        f"'{t.iloc[6, 1]}','{t.iloc[1, 3]}','{t.iloc[4, 3]}','{t.iloc[5, 3]}',"
        f"'{t.iloc[10, 1]}','{t.iloc[11, 1]}','{t.iloc[12, 1]}')"
    )
    update_sql = (
        f"UPDATE cooperation_info set short_name='{t.iloc[1, 1]}',"
        f"name='{t.iloc[2, 1]}', english_name='{t.iloc[3, 1]}',"
        f"legal_representative='{t.iloc[6, 1]}', address='{t.iloc[1, 3]}',"
        f"chairman='{t.iloc[4, 3]}', secratery='{t.iloc[5, 3]}',"
        f"main_business='{t.iloc[10, 1]}', business_scope='{t.iloc[11, 1]}',"
        f"introduction='{t.iloc[12, 1]}' "
        f"WHERE stock_code='{stock_code}'"
        )
    try:
        mysql.engine.execute(insert_sql)
    except Exception:
        mysql.engine.execute(update_sql)


def event_stratagy():
    # segment()
    header = mysqlHeader('root', '6414939', 'test')
    s = stratagy_new()
    s._init_database(header)
    s.run()


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


class EventRelationship(StockEventBase):
    def fetch_relation_sheet(self, stock_code):
        url = f"http://quotes.money.163.com/f10/jjcg_{stock_code}.html#01d03"


if __name__ == "__main__":
    # segment()
    header = mysqlHeader('root', '6414939', 'test')
    trade_date_list = ["20191113","20191114","20191115","20191118","20191119"]
    event = EventTradeDetail()
    event._init_database(header)
    stock_list = event.fetch_all_stock_list()
    for trade_date in trade_date_list:
        for stock in stock_list:
            print(stock, ":", trade_date)
            try:
                event.fetch_(stock, trade_date)
            except Exception:
                pass
