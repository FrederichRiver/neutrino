#!/usr/bin/python3

from torch.utils.data import Dataset
from libstock import EventStockPrice
from libmysql8 import mysqlHeader
import pandas as pd
import functools


class financeData(Dataset):
    def __init__(self):
        pass

    def __getitem__(self, index):
        return self.data[index], self.label[index]

    def __len__(self):
        return len(self.data)

    def _get_stock_data(self, code, field):
        header = mysqlHeader('root', '6414939', 'test')
        sp = EventStockPrice()
        sp._init_database(header)
        prices = sp.run(code, field)
        return prices


def ma(x, n):
    x['ma%s' % n] = x['close_price'].rolling(window=n).mean()
    return x.fillna(0.0)


ma7 = functools.partial(ma, n=7)
ma12 = functools.partial(ma, n=12)
ma26 = functools.partial(ma, n=26)
ma5 = functools.partial(ma, n=5)
ma10 = functools.partial(ma, n=10)
ma20 = functools.partial(ma, n=20)


def ema(df, n):
    df['%dema' % n] = df['close_price'].ewm(span=n).mean()
    return df.fillna(0.0)


ema12 = functools.partial(ema, n=12)
ema26 = functools.partial(ema, n=26)


def MACD(df):
    col = df.columns.values.tolist()
    if '12ema' not in col:
        df = ema(df, 12)
    if '26ema' not in col:
        df = ema(df, 26)
    df['MACD'] = df['12ema']-df['26ema']
    return df


class filter(object):
    def __init__(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    fd = financeData()
    t = fd._get_stock_data('SH600001', 'close_price, open_price, highest_price, lowest_price')

    print(t)
    print(ma(t,7))
    print(ma26(t))

    print(MACD(t))
