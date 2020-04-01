#!/usr/bin/python3

import re
import pandas as pd
import talib as ta
import numpy as np
from env import TIME_FMT
from lxml import etree
from libmysql8 import (mysqlBase, mysqlHeader)
from datetime import datetime
from form import formStockManager, formIncomeStatement, formBalance
from sqlalchemy.types import Date, DECIMAL, Integer, NVARCHAR
from libstock import StockEventBase
from env import global_header
from utils import RandomHeader


__version__ = '1.0.2-dev'


class StratagyBase2(StockEventBase):
    def __init__(self):
        super(StockEventBase, self).__init__()

    def fetch_data(self, stock_code):
        sql = f"select trade_date,open_price,close_price,\
            highest_price, lowest_price,\
            prev_close_price from {stock_code}"
        df = self.mysql.engine.execute(sql).fetchall()
        df = pd.DataFrame.from_dict(df)
        df = self._config(df)
        return df

    def run(self):
        df = self.fetch_data(stock_code)
        df['up'] = ta.MAX(df['high'], timeperiod=20).shift(1)
        df['down'] = ta.MIN(df['low'], timeperiod=10).shift(1)
        df['ATR'] = ta.ATR(df['high'], df['low'], df['close'], timeperiod=20)
        df['ret'] = df['close']/df['close'].shift(1)-1
        x1 = df['high'] > df['up']
        x2 = df['high'].shift(1) < df['up'].shift(1)
        x = x1 & x2
        y1 = df['low'] < df['down']
        y2 = df['low'].shift(1) > df['down'].shift(1)
        y = y1 & y2
        df.loc[x, 'signal'] = 'B'
        df.loc[y, 'signal'] = 'S'
        buy_date = (df.loc[df['signal'] == 'B'].index).strftime("%Y-%m-%d")
        sell_date = (df.loc[df['signal'] == 'S'].index).strftime("%Y-%m-%d")
        buy_close = df[df['signal'] == 'B'].close.round(2).tolist()
        sell_close = df[df['signal'] == 'S'].close.round(2).tolist()

    def _config(self, df):
        df.columns = ['trade_date', 'open', 'close', 'high', 'low', 'prev_close']
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df.set_index('trade_date', inplace=True)
        return df

    def profit(self):
        buy_index = df[df['close'] > df['down'].shift(1)].index
        # print(buy_index)
        df.loc[buy_index, 'close_signal'] = 1
        df['storage'] = df['close_signal'].shift(1)
        df['storage'].fillna(method='ffill', inplace=True)
        d = df[df['storage'] == 1].index[0]-timedelta(days=1)
        df = df.loc[d:].copy()
        df['ret'][0] = 0
        df['storage'][0] = 0
        df['strategy_value'] = (
            df['ret'].values*df['storage'].values+1.0).cumprod()
        df['index_value'] = (df['ret'].values+1.0).cumprod()
        df['sta_rate'] = df['strategy_value']/df1['strategy_value'].shift(1)-1
        df['index_rate'] = df.ret
        total_ret = df[['strategy_value', 'index_value']].iloc[-1]-1
        annual_ret = pow(1+total_ret, 250/len(df1))-1
        beta = df[['sta_rate', 'index_rate']].cov().iat[0, 1] / \
            df['index_rate'].var()
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

