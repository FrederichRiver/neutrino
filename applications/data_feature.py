#!/usr/bin/python3

from torch.utils.data import Dataset
from events import EventStockPrice
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
        sp =EventStockPrice()
        prices = sp.run(code, field)
        return prices


def ma(x, n):
    x['ma%s' % n] = x['close_price'].rolling(window= n).mean()
    return x.fillna(0.0)
    
ma7 = functools.partial(ma, n=7)
ma12 = functools.partial(ma, n=12)
ma26 = functools.partial(ma, n=26)

def ema(df, n):
    df['%dema'%n] = pd.ewma(df['close_price'], span=n)
    return df.fillna(0.0)
ema12 = functools.partial(ema, n=12)
ema26 = functools.partial(ema, n=26)

def MACD(df):
    col = df.columns.values.tolist()
    if '12ema' not in col:
        df=ema(df,12)
    if '26ema' not in col:
        df=ema(df,26)
    df['MACD']=df['12ema']-df['26ema']
    return df

if __name__ == '__main__':
    fd = financeData()
    t = fd._get_stock_data('SH600001', 'close_price, open_price, high_price, low_price')

    print(t)
    print(ma(t,7))
    print(ma26(t))

    #ema(t,12)
    #ema(t,26)
    print(MACD(t))
