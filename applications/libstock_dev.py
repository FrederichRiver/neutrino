#!/usr/bin/python3

import pandas as pd
import talib as ta
from env import TIME_FMT
from lxml import etree
from libmysql8 import (mysqlBase, mysqlHeader,
                       create_table_from_table)
from datetime import datetime
from form import formStockList
from sqlalchemy.types import Date, DECIMAL, Integer, NVARCHAR
from libstock import StockEventBase
__version__ = '1.3.11-dev'


class StratagyBase(StockEventBase):
    def __init__(self):
        super(StockEventBase, self).__init__()

    def fetch_data(self):
        pass

    def settle(self):
        pass


class InvestmentBase(object):
    def __init__(self):
        self.start_date = datetime.today()

    def settle(self):
        pass


def test(stock_code):
    print(stock_code)
    stock_conn = MySQLBase('root', '6414939', 'stock')
    sql = f"select trade_date,open_price,close_price,\
            highest_price, lowest_price,\
            prev_close_price from {stock_code}"
    res = stock_conn.session.execute(sql).fetchall()
    res = pd.DataFrame.from_dict(res)
    res.columns = ['trade_date', 'open', 'close', 'high',
                   'low', 'prev_close']
    res['trade_date'] = pd.to_datetime(res['trade_date'])
    res.set_index('trade_date', inplace=True)
    res['up'] = ta.MAX(res['high'], timeperiod=20).shift(1)
    res['down'] = ta.MIN(res['low'], timeperiod=10).shift(1)
    res['ATR'] = ta.ATR(res['high'], res['low'],
                        res['close'], timeperiod=20)
    res['ret'] = res['close']/res['close'].shift(1)-1
    # res = res[30:100]
    # res = res.drop(['highest', 'lowest' ], axis=1)
    # res= res.drop(['ATR'],axis =1)
    x1 = res['high'] > res['up']
    x2 = res['high'].shift(1) < res['up'].shift(1)
    x = x1 & x2
    y1 = res['low'] < res['down']
    y2 = res['low'].shift(1) > res['down'].shift(1)
    y = y1 & y2
    res.loc[x, 'signal'] = 'B'
    res.loc[y, 'signal'] = 'S'
    # print(res.shape[0])
    buy_date = (res.loc[res['signal'] == 'B'].index).strftime("%Y-%m-%d")
    sell_date = (res.loc[res['signal'] == 'S'].index).strftime("%Y-%m-%d")
    # print(buy_date)
    # print(sell_date)
    buy_close = res[res['signal'] == 'B'].close.round(2).tolist()
    sell_close = res[res['signal'] == 'S'].close.round(2).tolist()
    # print(buy_close)
    # print(sell_close)
    # res.plot()
    # plt.show()
    # use pyecharts lib
    # res = res[30:400]
    # print(res.head(10))
    from mpl_finance import candlestick_ochl as kplot
    from matplotlib.dates import date2num
    from datetime import timedelta
    """
    fig, ax = plt.subplots()
    plt.xticks(rotation=45)
    plt.yticks()
    ax.xaxis_date()
    data_list = []
    for dt, row in res.iterrows():
        t = date2num(dt)
        op, cl, high, low = row[:4]
        # print(dt, row[:4])
        data = (t, op, cl, high, low)
        data_list.append(data)
    try:
        kplot(ax, data_list,
              width=1.0, colorup='r', colordown='green', alpha=0.75)
    except Exception as e:
        pass
        # print(e)
    # plt.show()
    """
    stock_conn.session.close()
    buy_index = res[res['close'] > res['down'].shift(1)].index
    # print(buy_index)
    res.loc[buy_index, 'close_signal'] = 1
    res['storage'] = res['close_signal'].shift(1)
    res['storage'].fillna(method='ffill', inplace=True)
    d = res[res['storage'] == 1].index[0]-timedelta(days=1)
    df1 = res.loc[d:].copy()
    df1['ret'][0] = 0
    df1['storage'][0] = 0
    df1['strategy_value'] = (
        df1['ret'].values*df1['storage'].values+1.0).cumprod()
    df1['index_value'] = (df1['ret'].values+1.0).cumprod()
    df1['sta_rate'] = df1['strategy_value']/df1['strategy_value'].shift(1)-1
    df1['index_rate'] = df1.ret
    total_ret = df1[['strategy_value', 'index_value']].iloc[-1]-1
    annual_ret = pow(1+total_ret, 250/len(df1))-1
    beta = df1[['sta_rate', 'index_rate']].cov().iat[0, 1] / \
        df1['index_rate'].var()
    alpha = (annual_ret['strategy_value']-annual_ret['index_value']*beta)
    exReturn = df1['sta_rate']-0.03/250
    import numpy as np
    sharp_ratio = np.sqrt(len(exReturn))*exReturn.mean()/exReturn.std()
    print('total ret:', total_ret.values[0])
    print('annual ret:', annual_ret.values[0])
    print('beta:', beta)
    print('alpha:', alpha)
    print('sharp ratio:', sharp_ratio)
    return stock_code, total_ret.values[0], annual_ret.values[0], beta, alpha, sharp_ratio


def beta(df, df2):
    import numpy as np
    beta = np.cov(df, df2) / np.var(df2)
    return beta


class EventRehabilitation(StockEventBase):
    def rehabilitate(self, stock_code):
        """
        Main function, rehabilitation process.
        """
        try:
            # fetching data from mysql.
            sql = (
                "select trade_date,open_price,close_price,"
                "highest_price, lowest_price, prev_close_price,"
                f"amplitude from {stock_code}")
            result = self.mysql.session.execute(sql).fetchall()
            self.df = pd.DataFrame.from_dict(result)
            # data configging
            self._config_df()
            share = self._fetch_share(stock_code)
            self.df = pd.concat([self.df, share], axis=1, join='outer')
            # print(self.df.head(5))
            self.df.sort_index()
            self.df['reh'] = self.df['close']
            self.df.fillna(0, inplace=True)
            self.adjust_factor()
        except Exception:
            print(Exception)

    def adjust_factor(self):
        """
        Calculating adjust factor.
        Beta version.
        """
        self.df['factor'] = self.df['close']
        xr_flag = 0
        factor = 1.0
        for i in range(self.df.shape[0]):
            if i:
                if self.df.ix[i, 'dividend']+self.df.ix[i, 'bonus']+self.df.ix[i, 'increase']:
                    xr_flag = 2
                    factor = factor*self.df.ix[i-1, 'close']/self.df.ix[i, 'prev_close']
                else:
                    if xr_flag:
                        xr_flag -= 1
            self.df.ix[i, 'factor'] = factor
            self.df.ix[i, 'reh'] = self.df.ix[i, 'close']*factor
            if xr_flag:
                pass
                # print(
                #    self.df.index.T[i], self.df.ix[i, 'close'], self.df.ix[i, 'reh'], self.df.ix[i, 'factor'],
                #    self.df.ix[i, 'dividend'], self.df.ix[i, 'bonus'], self.df.ix[i, 'increase'])

    def _config_df(self):
        """
        Config dataframe, set data type, column index, etc.
        """
        # setting column index.
        self.df.columns = ['date', 'open', 'close', 'high', 'low', 'prev_close', 'amplitude']
        # setting data type.
        self.df['open'] = self.df['open'].astype(float)
        self.df['close'] = self.df['close'].astype(float)
        self.df['high'] = self.df['high'].astype(float)
        self.df['low'] = self.df['low'].astype(float)
        self.df['prev_close'] = self.df['prev_close'].astype(float)
        self.df['amplitude'] = self.df['amplitude'].astype(float)
        # convert date format from string to date.
        self.df = set_date_as_index(self.df)

    def _fetch_share(self, stock_code):
        """
        Getting interest data
        """
        # Querying data from mysql
        sql = (
            "SELECT xrdr_date, bonus, increase, dividend "
            f"FROM {stock_code}_interest")
        share = self.mysql.session.execute(sql).fetchall()
        # converting dict data to dataframe format
        share = pd.DataFrame.from_dict(share)
        # setting column index
        share.columns = ['date', 'bonus', 'increase', 'dividend']
        # converting data format and setting index
        share = set_date_as_index(share)
        return share

    def update_adjust_factor(self, stock_code):
        # first judge whether adjust factor has been calculated.
        for index, row in self.df.iterrows():
            # print(type(index), row['factor'])
            try:
                sql = (
                    f"update {stock_code} set trade_date='{index}',"
                    f"adjust_factor={row['factor']} "
                    f"where trade_date='{index}'")
                self.mysql.engine.execute(sql)
            except Exception:
                print(Exception)


def set_date_as_index(df):
    df['date'] = pd.to_datetime(df['date'], format=TIME_FMT)
    df.set_index('date', inplace=True)
    # exception 1, date index not exists.
    # exception 2, date data is not the date format.
    return df


if __name__ == '__main__':
    header = mysqlHeader('root', '6414939', 'test')
    reh = EventRehabilitation()
    reh._init_database(header)
    stock_list = reh.fetch_all_stock_list()
    for stock in stock_list:
        reh.rehabilitate(stock)
        reh.update_adjust_factor(stock)
