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
    def __init__(self, header):
        super(EventInterest, self).__init__(header)
        self.df = pd.DataFrame()

    def create_interest_table(self):
        """
        Initial interest table.
        """
        from venus.form import formInterest
        self.mysql.create_table_from_table(
                "stock_interest",
                formInterest.__tablename__,
                self.mysql.engine)

    def resolve_interest_table(self, stock_code:str):
        """
        Recognize interest table from html,
        returns a dataframe table.\n
        Used for batch insert.
        """
        import pandas as pd
        import numpy as np
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

    def batch_insert_interest_to_sql(self, df):
        from venus.stock_base import dataLine
        from jupiter.utils import ERROR
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
        from jupiter.utils import ERROR
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
                print(index, row)
                # sql = (
                #    f"update {stock_code} set adjust_factor={row['factor']} "
                #    f"where trade_date='{index}'")
                # self.mysql.engine.execute(sql)
            except Exception as e:
                ERROR((
                    f"Error occurs while updating {stock_code}, "
                    f"trade_date={index}, factor={row['factor']}"))
        # """

def test():
    from dev_global.env import GLOBAL_HEADER
    import numpy as np
    import re
    stock_code = 'SH601818'
    event = EventInterest(GLOBAL_HEADER) 

def test2():
    from dev_global.env import GLOBAL_HEADER
    import numpy as np
    import re
    import pandas as pd
    from datetime import date as dt
    stock_code = 'SH600000'
    event = StockEventBase(GLOBAL_HEADER)
    query1 = pd.DataFrame()
    query2 = pd.DataFrame()
    query1 = event.mysql.select_values(
        stock_code, 'trade_date,open_price,close_price, prev_close_price'
    )
    query1.columns = ['trade_date','open','close', 'prev_close']
    query1['trade_date'] = pd.to_datetime(query1['trade_date'])
    query1.set_index('trade_date',inplace=True)


    query2 = event.mysql.condition_select(
        'stock_interest', 'float_dividend,float_bonus,xrdr_date', f"char_stock_code='{stock_code}'"
    )
    query2.columns = ['dividend','bonus','xrdr_date']
    query2['xrdr_date'] = pd.to_datetime(query2['xrdr_date'])
    query2['trade_date'] = query2['xrdr_date']
    query2.set_index('trade_date',inplace=True)

    query1['comp'] = query1['close'] - query1['prev_close'].shift(-1)
    #print(query1[query1['comp']!=0])
    #print(query2.head(5))
    comb = pd.concat([query1,query2], axis=1)
    #print(comb[(comb['xrdr_date'].notnull()) | (comb['comp']!=0.0)])
    print(comb.loc[dt(2010,2,24):dt(2010,3,13),])

def test3():
    from dev_global.env import GLOBAL_HEADER
    import numpy as np
    import re
    import pandas as pd
    from datetime import date as dt
    stock_code = 'SH600022'
    event = StockEventBase(GLOBAL_HEADER)
    query1 = pd.DataFrame()
    query1 = event.mysql.select_values(
            stock_code, 'trade_date,open_price,close_price,highest_price,lowest_price, prev_close_price'
        )
    query1.columns = ['trade_date','open_price','close_price','highest_price','lowest_price', 'prev_close_price']
    query1.set_index('trade_date', inplace=True)
    print(query1.loc[dt(2009,11,5):dt(2010,2,23),])


def test4():
    from dev_global.env import GLOBAL_HEADER
    import numpy as np
    import re
    import pandas as pd
    from datetime import date as dt
    stock_code = 'SH600022'
    event = StockEventBase(GLOBAL_HEADER)
    stock_list = event.get_all_stock_list()
    for stock_code in stock_list:
        query1 = pd.DataFrame()
        query1 = event.mysql.select_values(
            stock_code, 'trade_date,open_price,close_price,highest_price,lowest_price, prev_close_price'
        )
        if not query1.empty:
            for index, row in query1.iterrows():
                if row[0] == 0 or row[1] == 0 or row[2] == 0 or row[3] == 0 or row[4] == 0 or row[5] == 0 :
                    print(stock_code, row[0], row[1],row[2],row[3],row[4], row[5])
            
if __name__ == "__main__":
    test3()   