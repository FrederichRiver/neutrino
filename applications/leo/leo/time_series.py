#!/usr/bin/python3
from venus.stock_base import StockEventBase


class Stratagy(StockEventBase):
    def baseline(self):
        import pandas as pd
        import math
        from dev_global.env import TIME_FMT
        df = self.mysql.select_values('SH000300', 'trade_date,close_price')
        # data cleaning
        df.columns = ['trade_date', 'close_price']
        pd.to_datetime(df['trade_date'], format=TIME_FMT)
        df.set_index('trade_date', inplace=True)
        # data constructing
        df['shift'] = df['close_price'].shift(1)
        df['amplitude'] = df['close_price'] / df['shift']
        df['ln_amplitude'] = df['amplitude'].apply(math.log)
        df.dropna(inplace=True)
        print(df.head(5))
        # plot
        plt = self.series_plot(df['ln_amplitude'])
        plt.show()

    def baseline_view(self):
        import pandas as pd
        import math
        from dev_global.env import TIME_FMT
        df = self.mysql.select_values(
            'SH000300',
            'trade_date,open_price,close_price,highest_price,lowest_price')
        # data cleaning
        df.columns = ['trade_date', 'open', 'close', 'high', 'low']
        pd.to_datetime(df['trade_date'], format=TIME_FMT)
        df.set_index('trade_date', inplace=True)
        # data constructing
        print(df.head(5))
        # plot
        plt = self.kplot(df[-50:])
        plt.show()

    def series_plot(self, df):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(df)
        ax.set_title('Shanghai 300 stocks', fontsize=18)
        ax.set_xlabel('date')
        ax.set_ylabel('index')
        return plt

    def kplot(self, df):
        import matplotlib.pyplot as plt
        from mpl_finance import candlestick_ochl as kplot
        from matplotlib.dates import date2num
        from datetime import timedelta
        fig, ax = plt.subplots()
        plt.xticks(rotation=45)
        plt.yticks()
        ax.xaxis_date()
        data_list = []
        for dt, row in df.iterrows():
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
        return plt


if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    event = Stratagy(GLOBAL_HEADER)
    # event.baseline()
    event.baseline_view()
