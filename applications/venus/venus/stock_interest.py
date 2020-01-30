#!/usr/bin/python3
import numpy as np
import pandas as pd
import requests
import time
from dev_global.env import CONF_FILE, GLOBAL_HEADER
from jupiter.utils import ERROR, read_url
from lxml import etree
from venus.stock_base import StockEventBase, dataLine
from venus.form import formInterest


__version__ = '1.1.3'


class EventInterest(StockEventBase):
    def create_interest_table(self):
        create_table_from_table(
                "stock_interest",
                formInterest.__tablename__,
                self.mysql.engine)

    def data_clean(self, df):
        for index, col in df.iteritems():
            try:
                if re.search('date', index):
                    df[index] = pd.to_datetime(df[index])
                elif re.search('int', index):
                    df[index] = pd.to_numeric(df[index])
                elif re.search('float', index):
                    df[index] = pd.to_numeric(df[index])
                elif re.search('char', index):
                    pass
                else:
                    pass
            except Exception:
                ERROR(
                    f"Error while record interest of {col['char_stock_code']}")
        return df

    def resolve_interest_table(self, stock_code):
        """
        Recognize interest table from html,
        return a dataframe table.
        Result -> tab (a Dataframe object)
        """
        url = read_url('URL_fh_163', CONF_FILE)
        url = url.format(stock_code[2:])
        result = pd.read_html(
            url, attrs={'class': 'table_bg001 border_box limit_sale'})
        tab = result[0]
        tab.columns = [
            'report_date', 'int_year', 'float_bonus',
            'float_increase', 'float_dividend',
            'record_date', 'xrdr_date', 'share_date']
        tab['char_stock_code'] = stock_code
        return tab

    def insert_interest_table_into_sql(self, stock_code):
        tab = self.resolve_table(stock_code)
        tab.replace(['--'], np.nan, inplace=True)
        tab.to_sql(
            'test_interest', self.mysql.engine.connect(),
            if_exists="append", index=False)

    def batch_insert_interest_to_sql(self, df):
        dataline = dataLine('test_interest')
        sql_list = dataline.insert_sql(df)
        for sql in sql_list:
            try:
                self.mysql.engine.execute(sql)
            except Exception:
                ERROR(f"Error while insert data : <{sql}>")


if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    import numpy as np
    import re
    stock_code = 'SH601818'
    pass
