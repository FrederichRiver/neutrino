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


def beta(df, df2):
    import numpy as np
    beta = np.cov(df, df2) / np.var(df2)
    return beta


class StratagyBase(StockEventBase):
    # def __init__(self, start_date, end_date, period):
    #    super(StockEventBase, self).__init__()

    def fetch_adjust_price(self, stock_code):
        """
        From local database, fetch adjust price.
        data format: DataFrame in pandas.
        data order like： close price, open price, low price, high price.
        """
        sql = f"SELECT stock_name,trade_date,close_price,adjust_factor from {stock_code}"
        result = self.mysql.engine.execute(sql)
        df = pd.DataFrame.from_dict(result)
        df.columns = ['stock_name', 'trade_date', 'close_price', 'adjust_factor']
        df.set_index('trade_date', inplace=True)
        df.fillna(0, inplace=True)
        for i in range(len(df)):
            if not df['adjust_factor'][i]:
                df['adjust_factor'][i] = df['adjust_factor'][i-1]
        df['close_price'] = df['close_price'] * df['adjust_factor']
        print(df)
        return df

    def plot(self, data):
        pass

    def select_stock(self):
        # last period profit
        last_period_profit = self.mysql.session.query(
            formIncomeStatement.stock_code,
            formIncomeStatement.r4_net_profit
        ).filter_by(report_period='2018-12-31')
        df4 = pd.DataFrame.from_dict(last_period_profit)
        df4.set_index('stock_code', inplace=True)
        df4.columns = ['last_year_profit']
        # profit
        net_profit = self.mysql.session.query(
            formIncomeStatement.stock_code,
            formIncomeStatement.r4_net_profit
        ).filter_by(report_period='2019-09-30')
        df = pd.DataFrame.from_dict(net_profit)
        df.set_index('stock_code', inplace=True)
        # roe
        result2 = self.mysql.session.query(
            formBalance.stock_code,
            formBalance.r6_total_equity
        ).filter_by(report_period='2019-09-30')
        df2 = pd.DataFrame.from_dict(result2)
        df2.set_index('stock_code', inplace=True)
        # stock name
        result3 = self.mysql.session.query(
            formStockManager.stock_code,
            formStockManager.stock_name
        )
        df3 = pd.DataFrame.from_dict(result3)
        df3.set_index('stock_code', inplace=True)
        # data processing
        df = pd.concat([df, df2], axis=1, join='outer')
        df = pd.concat([df, df4], axis=1, join='outer')
        df = pd.concat([df, df3], axis=1, join='inner')
        df['roe'] = df['r4_net_profit']/df['r6_total_equity']
        df = df[df['roe'] > 0.1]
        df = df[df['last_year_profit'] > 0]
        df = df[df['r4_net_profit'] > 0]
        for index, row in df.iterrows():
            if re.search(r'ST', row['stock_name']):
                df.drop(index, inplace=True)
        df.sort_values(by='roe', inplace=True, ascending=False)
        # print(df.head(5))
        stock_list = df.index.tolist()
        # print(stock_list)
        return stock_list

    def run(self, stock_code):
        from data_feature import ma5, ma10, ma20
        sql = f"SELECT stock_name,trade_date,close_price from {stock_code}"
        result = self.mysql.engine.execute(sql)
        df = pd.DataFrame.from_dict(result)
        df.columns = ['stock_name', 'trade_date', 'close_price']
        df.set_index('trade_date', inplace=True)
        ma5(df)
        ma10(df)
        ma20(df)
        df = df[-1:]
        # print(df)
        with open('stock_list', 'a') as f:
            if df['ma5'][-1] > df['ma10'][-1] > df['ma20'][-1]:
                line = stock_code + df['stock_name'][-1] + '\n'
                f.write(line)

    def choose_stock(self, upper_limit):
        import random
        stock_list = self.fetch_all_stock_list()
        n = random.randint(0, upper_limit)
        return stock_list[n]

    def fetch_stock_name(self, stock_code):
        sql = f"Select stock_name from stock_manager Where stock_code = '{stock_code}'"
        result = self.mysql.engine.execute(sql).fetchone()
        return result[0]

    def amp_3_day(self, stock_code):
        import datetime
        day = datetime.datetime.now() - datetime.timedelta(days = 10)
        # print(day.strftime(TIME_FMT))
        day_string = day.strftime(TIME_FMT)
        sql = f"Select amplitude, close_price from {stock_code} Where trade_date > '{day_string}'"
        result = self.mysql.engine.execute(sql)
        try:
            data = pd.DataFrame.from_dict(result)
            data = data.tail(3)
            amp2 = 0
            # print(amp2)
            price = sum(data[1])/3
            amp = sum(data[0])
        except Exception as e:
            # print(Exception, e)
            amp = 0
            amp2 = 0
            price = 0
        return amp, amp2, price


class target(object):
    def __init__(self):
        self.sigma = 0
        self.profit = 0


class targetGroup(object):
    def __init__(self, r, sigma):
        if len(r) != len(sigma):
            print("Dimensions not equal.\n")
        else:
            self.r = np.array(r)
            self.sigma = np.array(sigma)

    def run(self, x):
        pass


def test():
    header = mysqlHeader('root', '6414939', 'test')
    event = StratagyBase()
    event._init_database(header)
    stock_list = event.select_stock()
    with open('data0116.log', 'w') as f:
        for stock in stock_list:
            name = event.fetch_stock_name(stock)
            amp, amp2, price = event.amp_3_day(stock)
            # print(stock, name, amp, amp2)
            if amp > 8:
                line = stock + ': ' + name + ': ' + str(amp) + '\n'
                f.write(line)


def test2():
    # calculate cov of assets.
    header = mysqlHeader('root', '6414939', 'test')
    event = StratagyBase()
    event._init_database(header)
    stock_data = pd.DataFrame()
    stock_list = ['SH601818', 'SZ002230', 'SZ002460', 'SZ300146']
    for stock in stock_list:
        sql = f"SELECT trade_date, amplitude from {stock} WHERE (trade_date>'2019-12-01' AND trade_date<'2020-01-07')"
        result = event.mysql.engine.execute(sql).fetchall()
        df = pd.DataFrame.from_dict(result)
        df.columns = ['trade_date', stock]
        df.set_index('trade_date', inplace=True)
        stock_data = pd.concat([stock_data, df], axis=1, join='outer', sort=False)
    # Cov calculation
    print(stock_data.cov())


def test3():
    # numpy test.
    import numpy.matlib
    a = np.array([[1, 2], [3, 4]])
    print(a)
    b = np.linalg.inv(a)
    print(b)
    c = a * b
    c = np.dot(a, b)
    print(c)


def solve(r, Cov):
    E = np.linalg.inv(Cov)
    L = numpy.matlib.ones((1, 5))
    # a = r.T * int(Cov) * r
    # b = r.T * int(Cov) * 1
    # c = 1.T * int(Cov) * 1
    a, b, c
    miu = b/c
    lamda1 = 1
    lamda2 = 2
    w = lamda1 * E * r + lamda2*E*L
    return miu, sigma, w


class MPTBase(StockEventBase):
    def __init__(self):
        super(MPTBase, self).__init__()
        # asset data group
        self.data = None
        # cov matrix
        self.cov = None
        self.beta = 0.0
        self.sharpe_m = 0.0
        self.none_risk_profit = 0.0
        self.asset_group = {}

    def solve_frontier(self):
        pass

    def fetch_data(self):
        pass

    def sh50_solver(self, header):
        import requests
        url = f"http://www.sse.com.cn/market/sseindex/indexlist/constlist/index.shtml?COMPANY_CODE=000016&cfg=yes&INDEX_Code=000016"
        html = self.fetch_html_object(url, header)
        table = html.xpath("//table[@class='table search_cfList searchCC']")
        table = etree.tostring(table[0]).decode()
        result = pd.read_html(table)
        print(result)


def test_event():
    rh = RandomHeader()
    event = MPTBase()
    event._init_database(global_header)
    event.sh50_solver(rh())


if __name__ == '__main__':
    test()
    """
    test_event()
    event = StockEventBase()
    event._init_database(global_header)
    stock_list = event.fetch_all_stock_list()
    for stock in stock_list:
        sql = (
            f"insert into stock_index "
            f"(stock_code) values ('{stock}')"
            )
        event.mysql.engine.execute(sql)
    """
