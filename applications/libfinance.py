#!/usr/bin/env python3

from form import formFinanceTemplate
import requests
from libstock import StockEventBase, codeFormat
from libmysql8 import mysqlHeader
import pandas as pd
import re
from sqlalchemy.types import Date, DECIMAL, Integer, NVARCHAR

__version__ = '1.0.2'


class EventFinanceReport(StockEventBase):
    def __init__(self):
        super(StockEventBase, self).__init__()
        self.coder = codeFormat()

    def _get_finance_report_from_net_ease(self, url):
        """
        read csv data and return a dataframe object.
        """
        data = pd.read_csv(url, encoding='gb18030')
        data = self._config(data)
        return data

    def _config(self, d):
        d = d.T
        columns = ['d1', 'd2', 'd3', 'r1', 'r2', 'r3', 'd7', 'd8',\
            'd9', 'r4', 'd11', 'd12', 'd13', 'r5', 'd15', 'r6',\
            'd17', 'd18', 'r7']
        d.columns = columns
        d.drop(d.index[[0, -1]], axis=0, inplace=True)
        for c in d.columns:
            if re.match(r'^d', c):
                d.drop([c], axis=1, inplace=True)
        d.replace('--', 0, inplace=True)
        d = d.apply(pd.to_numeric)
        return d

    def update_summary(self, stock_code):
        stock_code = '601818'
        url = f"http://quotes.money.163.com/service/zycwzb_{stock_code}.html?type=report"
        data = self._get_finance_report_from_net_ease(url)
        c = self._config_column()
        for index, row in data.iterrows():
            query_sql = f"SELECT * from summary where report_period='{index}'"
            query_result = event.mysql.engine.execute(query_sql).fetchall()
            if query_result:
                sql = (
                    f"UPDATE summary set {c['r1']}={row['r1']},"
                    f"{c['r4']}={row['r4']},{c['r5']}={row['r5']},"
                    f"{c['r6']}={row['r6']},{c['r7']}={row['r7']}"
                    f" WHERE report_period='{index}'")
            else:
                sql = (
                    "Insert into summary (report_period, "
                    f"{c['r1']}, {c['r4']}, {c['r5']}, {c['r6']}, {c['r7']}) "
                    f"VALUES ('{index}', {row['r1']}, "
                    f"{row['r4']}, {row['r5']}, {row['r6']}, {row['r7']})")
            event.mysql.engine.execute(sql)

    def _config_column(self):
        column = {
            'r1': 'r1_revenue',
            'r4': 'r4_net_profit',
            'r5': 'r5_total_asset',
            'r6': 'r7_total_liability',
            'r7': 'r9_roe'}
        return column


def event():
    stock_code = '601818'
    url = f"http://quotes.money.163.com/service/zycwzb_{stock_code}.html?type=report"
    header = mysqlHeader('root', '6414939', 'test')
    event = EventFinanceReport()
    event._init_database(header)
    d = event._get_finance_report_from_net_ease(url)
    d = d.T
    columns = ['d1', 'd2', 'd3', 'r1','r2','r3','d7','d8','d9','r4','d11','d12','d13','r5','d15','r6','d17','d18','r7']
    d.columns = columns
    d.drop(d.index[[0, -1]], axis=0, inplace=True)
    for c in d.columns:
        if re.match(r'^d', c):
            d.drop([c], axis=1, inplace=True)
    r1 = 'r1_revenue'
    r4 = 'r4_net_profit'
    r5 = 'r5_total_asset'
    r6 = 'r7_total_liability'
    r7 = 'r9_roe'
    d.replace('--', 0, inplace=True)
    d = d.apply(pd.to_numeric)
    d = d/100
    for index, row in d.iterrows():
        query_sql = f"SELECT * from summary where report_period='{index}'"
        query_result = event.mysql.engine.execute(query_sql).fetchall()
        if query_result:
            sql = (
                f"UPDATE summary set {r1}={row['r1']},"
                f"{r4}={row['r4']},{r5}={row['r5']},{r6}={row['r6']},{r7}={row['r7']}"
                f" WHERE report_period='{index}'")
        else:
            sql = (
                f"Insert into summary (report_period, {r1}, {r4}, {r5}, {r6}, {r7}) "
                f"VALUES ('{index}', {row['r1']}, {row['r4']}, {row['r5']}, {row['r6']}, {row['r7']})")
        event.mysql.engine.execute(sql)


if __name__ == "__main__":
    header = mysqlHeader('root', '6414939', 'test')
    event = EventFinanceReport()
    event._init_database(header)
    stock_list = event.fetch_all_stock_list()
    for stock in stock_list:
        print(stock[2:])
    event.update_summary('601818')
