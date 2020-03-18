#!/usr/bin/python3

from venus.stock_base import StockEventBase
from dev_global.env import GLOBAL_HEADER
import matplotlib.pyplot as plt
event = StockEventBase(GLOBAL_HEADER)
event.stock_list = event.get_all_stock_list()
result = []
for stock_code in event.stock_list:
    try:
        # stock_code = 'SH600000'
        df = event.mysql.select_values(stock_code, 'close_price')
        df.columns = ['close']
        # print(df.head(10))
        df['MA5'] = df['close'].rolling(5).mean()
        df['MA10'] = df['close'].rolling(10).mean()
        df['MA20'] = df['close'].rolling(20).mean()
        # df[-30:].plot()
        # plt.show()
        # print(df.iloc[-1:])

        # if df['MA20'].values[-1] < df['close'].values[-1] < 1.05 * df['MA20'].values[-1]:
        if df['MA5'].values[-1] > df['MA10'].values[-1] > df['MA20'].values[-1]:
            print(stock_code)
            result.append(stock_code)
    except Exception as e:
        print(e)
with open('stock_list', 'w+') as f:
    for stock_code in result:
        f.writelines(stock_code + '\n')
    f.close()
