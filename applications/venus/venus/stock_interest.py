#!/usr/bin/python3
import numpy as np
import pandas as pd
import requests
import time
from dev_global.env import CONF_FILE, GLOBAL_HEADER
from jupiter.utils import ERROR, read_url
from lxml import etree
from venus.stock_base import StockEventBase
from venus.form import formInterest


__version__ = '1.1.2'


class EventInterest(StockEventBase):
    def create_interest_table(self):
        create_table_from_table(
                "stock_interest",
                formInterest.__tablename__,
                self.mysql.engine)

    def record_interest(self):
        self.fetch_all_stock_list()
        for stock_code in self.stock_list:
            # stock code format: SH600000
            try:
                t = Thread(
                    target=self.sub_insert_interest_into_sql,
                    args=(stock_code,),
                    name=stock_code,
                    daemon=True)
                t.start()
                self.sub_insert_interest_into_sql(stock_code)
                time.sleep(1)
            except Exception:
                ERROR(f"Error while recording interest of {stock_code}")

    def sub_insert_interest_into_sql(self, stock_code):
        tab = self.resolve_table(stock_code)
        tab.replace(['--'], np.nan, inplace=True)
        tab.to_sql(
            'test_interest', self.mysql.engine.connect(),
            if_exists="append", index=False)

    def _resolve_dividend(self, stock_code):
        # fetch data table
        _, url = read_json('URL_fh_163', CONF_FILE)
        url = url.format(stock_code[2:])
        content = requests.get(url, timeout=3)
        html = etree.HTML(content.text)
        table = html.xpath(
            "//table[@class='table_bg001 border_box limit_sale']")
        share_table = table[0].xpath(".//tr")
        table_name = f"{stock_code}_interest"
        dt = DataLine()
        # resolve the data table
        for line in share_table:
            data_line = line.xpath(".//td/text()")
            if len(data_line) > 6:
                data_key, sql = dt.resolve(data_line, table_name)
                query = (f"SELECT * from {table_name} where "
                         f"report_date='{data_key}'")
                result = self.mysql.session.execute(query).fetchall()
                if not result:
                    self.mysql.session.execute(sql)
                    self.mysql.session.commit()

    def resolve_table(self, stock_code):
        url = read_url('URL_fh_163', CONF_FILE)
        url = url.format(stock_code[2:])
        result = pd.read_html(
            url, attrs={'class': 'table_bg001 border_box limit_sale'})
        tab = result[0]
        tab.columns = [
            'report_date', 'year', 'bonus', 'increase', 'dividend',
            'record_date', 'xrdr_date', 'share_date']
        tab['stock_code'] = stock_code
        return tab

    def insert_interest_to_sql(self, df):
        dt = dataLine(df, 'test_interest')
        sql_list = dt.insert_sql()
        for sql in sql_list:
            try:
                self.mysql.engine.execute(sql)
            except Exception:
                print(Exception)


if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    import numpy as np
    import re
    stock_code = 'SH601818'
    event = EventInterest(GLOBAL_HEADER)
    tab = event.resolve_table(stock_code)
    tab.replace(['--'], np.nan, inplace=True)

    for index, col in tab.iteritems():
        if re.search('date', index):
            tab[index] = pd.to_datetime(tab[index])
        else:
            try:
                tab[index] = pd.to_numeric(tab[index])
            except Exception:
                pass
        # tab[index].fillna(0, inplace=True)
    # print(tab.dtypes)
    """
    for index, row in tab.iterrows():
        for label in tab.columns:
            print(row[label], test(row[label]))
    # print(tab)
    """
    event.insert_interest_to_sql(tab)
    # dt = dataLine(tab, 'test_interest')
    # dt.insert_sql()
    """
    content = requests.get(url, timeout=3)
    html = etree.HTML(content.text)
    table = html.xpath(
            "//table[@class='table_bg001 border_box limit_sale']")
    share_table = table[0].xpath(".//tr")
    table_name = f"{stock_code}_interest"
    dt = DataLine()
    # resolve the data table
    for line in share_table:
        data_line = line.xpath(".//td/text()")
        if len(data_line) > 6:
            data_key, sql = dt.resolve(data_line, table_name)
            query = (f"SELECT * from {table_name} where "
                     f"report_date='{data_key}'")
            result = self.mysql.session.execute(query).fetchall()
            if not result:
                self.mysql.session.execute(sql)
                self.mysql.session.commit()
    """
