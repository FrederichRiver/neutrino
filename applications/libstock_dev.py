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
__version__ = '1.3.9-dev'


class StratagyBase(StockEventBase):
    def __init__(self):
        super(StockEventBase, self).__init__()

    def fetch_data(self):
        pass

    def settle(self):
        pass

    def reha(self):
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


class EventRehabilitation(StockEventBase):
    def rehabilitate(self, stock_code):
        sql = (
            "select trade_date,open_price,close_price,"
            "highest_price, lowest_price, prev_close_price,"
            f"amplitude from {stock_code}")
        result = self.mysql.session.execute(sql).fetchall()
        self.df = pd.DataFrame.from_dict(result)
        self._config_df()
        share = self._fetch_share(stock_code)
        self.df = pd.concat([self.df, share], axis=1, join='outer')
        self.df.sort_index()
        self.df['reh'] = self.df['close']
        self.df.fillna(0, inplace=True)
        self.factor1()

    def factor1(self):
        self.df['factor'] = self.df['close']
        # res = res[:700]
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
                print(
                    self.df.index.T[i], self.df.ix[i, 'close'], self.df.ix[i, 'reh'], self.df.ix[i, 'factor'],
                    self.df.ix[i, 'dividend'], self.df.ix[i, 'bonus'], self.df.ix[i, 'increase'])

    def _config_df(self):
        self.df.columns = ['date', 'open', 'close', 'high', 'low', 'prev_close', 'amplitude']
        self.df['open'] = self.df['open'].astype(float)
        self.df['close'] = self.df['close'].astype(float)
        self.df['high'] = self.df['high'].astype(float)
        self.df['low'] = self.df['low'].astype(float)
        self.df['prev_close'] = self.df['prev_close'].astype(float)
        self.df['amplitude'] = self.df['amplitude'].astype(float)
        # print(res.dtypes)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df.set_index('date', inplace=True)

    def _fetch_share(self, stock_code):
        sql2 = (
            "SELECT xrdr_date, bonus, increase, dividend "
            f"FROM {stock_code}_interest")
        share = self.mysql.session.execute(sql2).fetchall()
        share = pd.DataFrame.from_dict(share)
        share.columns = ['date', 'bonus', 'increase', 'dividend']
        share['date'] = pd.to_datetime(share['date'])
        share.set_index('date', inplace=True)
        return share


if __name__ == '__main__':
    header = mysqlHeader('root', '6414939', 'test')
    reh = EventRehabilitation()
    reh._init_database(header)
    stock_list = reh.fetch_all_stock_list()
    for stock in stock_list:
        reh.rehabilitate(stock)
