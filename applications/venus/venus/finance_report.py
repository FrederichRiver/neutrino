#!/usr/bin/python3
import numpy as np
import pandas as pd
from venus.stock_base import StockEventBase, dataLine
from jupiter.utils import read_url, CONF_FILE, trans


class EventFinanceReport(StockEventBase):
    def update_balance(self, stock_code):
        # get url
        url = read_url("URL_balance", CONF_FILE)
        url = url.format(stock_code[2:])
        # get data
        df = self.get_balance_sheet(stock_code)
        if not df.empty:
            dataline = dataLine('balance_sheet')
            try:
                insert_sql_list = dataline.insert_sql(df)
            except Exception as e:
                print(e)
        for sql in insert_sql_list:
            print(sql)

    def get_balance_sheet(self, stock_code):
        """
        read csv data and return a dataframe object.
        """
        from venus.form import balance_column
        from jupiter.utils import data_clean
        # config file is a url file.
        # _, url = read_json('URL_163_MONEY', CONF_FILE)
        url = read_url("URL_balance", CONF_FILE)
        url = url.format(stock_code[2:])
        df = pd.read_csv(url, encoding='gb18030')
        if not df.empty:
            df = df.T
            result = df.iloc[1:]
        else:
            result = df
        result.replace(['--'], np.nan, inplace=True)
        print(result.iloc[-1:].index)
        result.drop(result.iloc[-1:].index, axis=0, inplace=True)
        # result.columns = ['c'+str(i) for i in range(108)]
        result.columns = balance_column
        # result.loc[:, ('char_stock_code')] = stock_code
        result = data_clean(result)
        return result


if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    stock_code = 'SH601818'
    event = EventFinanceReport(GLOBAL_HEADER)
    event.update_balance(stock_code)
