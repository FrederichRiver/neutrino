#!/usr/bin/python3

from venus.stock_base import StockEventBase

class dev(StockEventBase):
    def __init__(self, stock_code, header):
        super(dev, self).__init__(header)
        self.stock_code = stock_code

    def get_data(self):
        import pandas as pd
        from talib.abstract import SMA
        import talib as ta
        import numpy as np
        from datetime import date as dt
        result = self.mysql.select_values(self.stock_code, 'trade_date,close_price')
        result.columns = ['trade_date','close_price']
        result['trade_date'] = pd.to_datetime(result['trade_date'])
        
        result.set_index('trade_date', inplace=True)
        
        result['MA5'] = ta.SMA(result.close_price, timeperiod=5) 
        result['MA10'] = ta.SMA(result.close_price, timeperiod=10) 
        result['MA20'] = ta.SMA(result.close_price, timeperiod=20) 
        result['MA60'] = ta.SMA(result.close_price, timeperiod=60)
        result['MA120'] = ta.SMA(result.close_price, timeperiod=120) 
        result['MA250'] = ta.SMA(result.close_price, timeperiod=250) 
        x1 = result['MA5'] > result['MA10']
        x2 = result['MA5'].shift(-1) < result['MA10']
        y = x1 & x2
        result.loc[y, 'signal'] = 'B'
        x1 = result['MA5'] < result['MA10']
        x2 = result['MA5'].shift(-1) > result['MA10']
        y = x1 & x2
        result.loc[y, 'signal'] = 'S'
        
        flag = 'S'
        own = False
        value = 100.0
        for index, row in result.iterrows():
            
            if row['signal'] == 'S':
                if own:
                    value += row['close_price']
                    own = False
                    print(f"{index}, sell,",value)
            if row['signal'] == 'B':
                if not own:
                    value -= row['close_price']
                    own = True
                    print(f"{index}, buy,",value)
            
        # print(result[(result['signal']=='B') | (result['signal']=='S')])
        # print(result.loc[dt(2020,3,3):dt(2020,3,9)])
        print(value)

if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    event = dev('SH600000', GLOBAL_HEADER)
    event.get_data()
