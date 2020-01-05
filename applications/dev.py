#!/usr/bin/python3
# from statsmodels.tsa.arima_model import ARIMA
import datetime
import pandas as pd
import numpy as np
import requests
import time
import random
from env import global_header
from libmysql8 import mysqlHeader, mysqlBase
from libstock import wavelet_nr, StockEventBase, str2zero
from libstratagy import StratagyBase
from lxml import etree
from data_feature import ma
from form import formFinanceTemplate, formBalance
from utils import str2number
from utils import RandomHeader, read_url

__version__ = '1.6.8-beta'


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


class Stratagy1(StockEventBase):
    def fetch_report_period(self):
        """
        Return : period, q1, q2, q3, q4
        """
        now = datetime.datetime.now()
        year = range(1990, now.year)
        q1 = [f"{y}-03-31" for y in year]
        q2 = [f"{y}-06-30" for y in year]
        q3 = [f"{y}-09-30" for y in year]
        q4 = [f"{y}-12-31" for y in year]
        period = q1 + q2 + q3 + q4
        return period, q1, q2, q3, q4

    def fetch_data(self):
        period[0] = self.fetch_report_period()
        for p in period:
            print(p)
            try:
                sql = (
                    "SELECT stock_code,r4_net_profit,r3_5_income_tax,r2_5_finance_expense,r1_1_revenue "
                    f"from income_statement_template where report_period='{p}'"
                )
                income_statement = self.mysql.engine.execute(sql).fetchall()
                income_statement = pd.DataFrame.from_dict(income_statement)
                if not income_statement.empty:
                    income_statement.set_index(0, inplace=True)
                    income_statement.columns = ['net_profit', 'income_tax', 'finance_expense', 'revenue']
                sql2 = (
                    "SELECT stock_code,r1_assets,r1_1_bank_and_cash,r5_3_accounts_payable "
                    f"from balance_sheet_template where report_period='{p}'"
                )
                balance_sheet = self.mysql.engine.execute(sql2).fetchall()
                balance_sheet = pd.DataFrame.from_dict(balance_sheet)
                if not balance_sheet.empty:
                    balance_sheet.set_index(0, inplace=True)
                    balance_sheet.columns = ['asset', 'bank_cash', 'accout_payable']
                result = pd.concat([income_statement, balance_sheet], axis=1, join='outer', sort= False)
                if not result.empty:
                    result['EBIT'] = (result['net_profit'] + result['income_tax'] + result['finance_expense'])/result['revenue']
                    result['NOPLAT'] = result['EBIT']*(1-0.3)
                    result['ROIC'] = result['NOPLAT']
                    result[np.isinf(result)] = np.nan
                    result.dropna(inplace=True)
                    print(result.head(5))
                    for index, row in result.iterrows():
                        insert_sql = (
                            "INSERT INTO finance_factor ("
                            "stock_code, report_period, ebit, roic)"
                            "VALUES ( "
                            f"'{index}','{p}',{row['EBIT']},{row['ROIC']})"
                            )
                        update_sql = (
                            f"UPDATE finance_factor set stock_code='{index}',"
                            f"report_period='{p}', ebit={row['EBIT']},"
                            f"roic={row['ROIC']} "
                            f"WHERE stock_code='{index}' and report_period='{p}'"
                            )
                        try:
                            # print('Insert:', index)
                            self.mysql.engine.execute(insert_sql)
                        except Exception:
                            # print('Update', index)
                            self.mysql.engine.execute(update_sql)
            except Exception as e:
                print('Error:', e)


class TradeDate(object):
    def chinese_holiday(self, year):
        holiday = [
            (year, 1, 1), (year, 1, 2), (year, 1, 3),
            (year, 4, 5), (year, 5, 1), (year, 5, 2),
            (year, 5, 3), (year, 10, 1), (year, 10, 2),
            (year, 10, 3), (year, 10, 4), (year, 10, 5),
            (year, 10, 6), (year, 10, 7)
            ]
        return holiday


def delay(delta):
    time.sleep(random.randint(0, delta))


def str2float(content):
    import re
    content = content.replace(',', '')
    try:
        result = float(content)
    except Exception:
        result = 0
    # print(type(result))
    return result


if __name__ == "__main__":
    # segment()
    from env import global_header
    from utils import RandomHeader
    """
    td = TradeDate()
    days = td.chinese_holiday(2019)
    print('yes') if (2019, 5, 3) in days else print('no')
    """
    event = TotalStock()
    rh = RandomHeader()
    event._init_database(global_header)
    # event.update_stock_structure('SZ002230')
    event.stock_list = event.fetch_all_stock_list()
    # event.update_stock_structure('SH600000')
    # event.calculate_stock_structure('SH600001')
    for stock in event.stock_list:
        print(stock)
        event.hexun_stock_structure(stock, rh())
        event.calculate_stock_structure(stock)
