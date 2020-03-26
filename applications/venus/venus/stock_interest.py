#!/usr/bin/python3
import numpy as np
import pandas as pd
import requests
import time
from dev_global.env import CONF_FILE, GLOBAL_HEADER, TIME_FMT
from jupiter.utils import ERROR, read_url, set_date_as_index, data_clean
from lxml import etree
from venus.stock_base import StockEventBase
from venus.stock_base import dataLine
from venus.form import formInterest


__version__ = '1.2.4'


class EventInterest(StockEventBase):
    """
    """
    def create_interest_table(self):
        """
        Initial interest table.
        """
        from venus.form import formInterest
        self.mysql.create_table_from_table(
                "stock_interest",
                formInterest.__tablename__,
                self.mysql.engine)

    def resolve_interest_table(self, stock_code):
        """
        Recognize interest table from html,
        return a dataframe table.
        Result -> tab (a Dataframe object)
        Used for batch insert.
        """
        import pandas as pd
        from jupiter.utils import ERROR, read_url, data_clean
        url = read_url('URL_fh_163', CONF_FILE)
        url = url.format(stock_code[2:])
        # result is a list of DataFrame table.
        result = pd.read_html(
            url, attrs={'class': 'table_bg001 border_box limit_sale'})
        if result:
            tab = result[0]
            tab.columns = [
                'report_date', 'int_year', 'float_bonus',
                'float_increase', 'float_dividend',
                'record_date', 'xrdr_date', 'share_date']
            tab['char_stock_code'] = stock_code
            tab.replace(['--'], np.nan, inplace=True)
            # change column type according to their pre_fix.
            tab = data_clean(tab)
        else:
            tab = pd.DataFrame()
        return tab

    def insert_interest_table_into_sql(self, stock_code):
        tab = self.resolve_interest_table(stock_code)
        tab.replace(['--'], np.nan, inplace=True)
        tab.to_sql(
            'stock_interest', self.mysql.engine.connect(),
            if_exists="append", index=False)

    def batch_insert_interest_to_sql(self, df):
        from venus.stock_base import dataLine
        if not df.empty:
            dataline = dataLine('stock_interest')
            sql_list = dataline.insert_sql(df)
            for sql in sql_list:
                try:
                    self.mysql.engine.execute(sql)
                except Exception:
                    ERROR(f"Error while insert data : <{sql}>")

    def price_adjust(self, stock_code):
        import datetime
        select_col = (
            "trade_date,close_price,prev_close_price"
        )
        select_col2 = "xrdr_date,float_bonus,float_increase,float_dividend"
        select_cond2 = f"char_stock_code='{stock_code}'"
        try:
            # get trade data.
            self.df = self.mysql.select_values(stock_code, select_col)
            share = self.mysql.condition_select(
                'stock_interest', select_col2, select_cond2)
            # print(share)
            # data config
            self.df.columns = ['date', 'close', 'prev_close']
            share.columns = ['date', 'bonus', 'increase', 'dividend']
            share = set_date_as_index(share)
            print(share)
            self.df = set_date_as_index(self.df)
            self.df = pd.concat([self.df, share], axis=1)
            self.df['close_shift'] = self.df['close'].shift(1)
            self.df['factor'] = 1.0
            # calculate adjust factor
            self.df['temp_factor'] = self.df['close_shift']/self.df['prev_close']
            # calculate price adjust factor day by day.
            f = 1.0
            for index, row in self.df.iterrows():
                if row['temp_factor'] > 1:
                    f *= row['temp_factor']
                row['factor'] = f
            self.df['adjust_close'] = self.df['close'] * self.df['factor']
            # print(self.df)
            self.df.drop(["bonus", "increase"], axis=1, inplace=True)
            # print(self.df[self.df['temp_factor'] > 1])
            print(self.df[185:195])
            print(self.df.tail(5))
        except Exception:
            ERROR(f"Error while calculate price adjust facort of {stock_code}")
        return self.df

    def update_adjust_factor(self, stock_code):
        select_col = "trade_date,adjust_factor,close_price"
        select_condition = "adjust_factor is null"
        select_condition = "1"
        # get trade data.
        adjust_factor = self.mysql.condition_select(
            stock_code, select_col, select_condition)
        adjust_factor.columns = ['date', 'adjust_factor', 'close_price']
        adjust_factor = set_date_as_index(adjust_factor)
        update_factor = pd.concat([adjust_factor, self.df['factor']], axis=1)
        update_factor.dropna(
            subset=['close_price'], how='any', axis=0, inplace=True)
        # print(update_factor)
        """
        # first judge whether adjust factor has been calculated.
        """
        # """
        for index, row in update_factor.iterrows():
            # print(type(index), row['factor'])
            try:
                pass
                # sql = (
                #    f"update {stock_code} set adjust_factor={row['factor']} "
                #    f"where trade_date='{index}'")
                # self.mysql.engine.execute(sql)
            except Exception as e:
                ERROR((
                    f"Error occurs while updating {stock_code}, "
                    f"trade_date={index}, factor={row['factor']}"))
        # """


if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    import numpy as np
    import re
    stock_code = 'SH601818'
    event = EventInterest(GLOBAL_HEADER)
    # event.insert_interest_table_into_sql('SZ002230')
    df = event.resolve_interest_table('SZ000625')
    print(df.info())
    event.batch_insert_interest_to_sql(df)
    # event.price_adjust(stock_code)
    # event.update_adjust_factor(stock_code)
