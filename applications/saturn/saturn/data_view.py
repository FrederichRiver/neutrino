#!/usr/bin/python3
from venus.stock_base import StockEventBase


class EventView(StockEventBase):
    def get_basic_index(self, stock_code):
        import pandas as pd
        import math
        from dev_global.env import TIME_FMT
        df = self.mysql.select_values(
            stock_code,
            'trade_date,open_price,close_price,highest_price,lowest_price,volume')
        # data cleaning
        df.columns = ['trade_date', 'open', 'close', 'high', 'low', 'volume']
        pd.to_datetime(df['trade_date'], format=TIME_FMT)
        df.set_index('trade_date', inplace=True)
        # data constructing
        # print(df.head(5))
        LEN = 70
        plt, ax1, ax2 = self.kplot(df[-LEN:])
        ma_list = [5, 20, 60]
        for ma in ma_list:
            df[f"MA{ma}"] = df['close'].rolling(ma).mean()
            ax1.plot(df[f"MA{ma}"][-LEN:])
        plt.rcParams['font.sans-serif'] = [u'SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # plt.show()
        img_path = f"/var/www/neutrino/static/images/{stock_code}.png"
        plt.savefig(img_path, format='png')

    def kplot(self, df):
        import matplotlib.pyplot as plt
        from mpl_finance import candlestick_ochl as candleplot
        from matplotlib.dates import date2num
        from datetime import timedelta
        import pandas
        import matplotlib.gridspec as mg
        gs = mg.GridSpec(3, 1)
        fig, (ax1, ax2) = plt.subplots(2, sharex=True)
        # plt.xticks(rotation=45)
        plt.yticks()
        ax1 = plt.subplot(gs[: 2, :])
        ax2 = plt.subplot(gs[2:, :])
        ax1.set_title('Shanghai 300')
        ax1.xaxis_date()
        ax1.set_ylabel('Index')
        data_list = []
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("Input param df is not type of DataFrame.")
        for dt, row in df.iterrows():
            t = date2num(dt)
            op, cl, high, low = row[:4]
            # print(dt, row[:4])
            data = (t, op, cl, high, low)
            data_list.append(data)
        try:
            candleplot(
                ax1, data_list,
                width=1.0,
                colorup='r', colordown='green', alpha=1)
        except Exception as e:
            pass
        for index, row in df.iterrows():
            if(row['close'] >= row['open']):
                ax2.bar(index, row['volume'], width=0.8, color='red')
            else:
                ax2.bar(index, row['volume'], width=0.8, color='green')
        # plt.bar(df.index, df['volume'], width=1)
        ax2.set_title('Volume')
        ax2.xaxis_date()
        return plt, ax1, ax2

    def kplot2(self, df):
        import matplotlib.pyplot as plt
        from mpl_finance import candlestick_ochl as candleplot
        from matplotlib.dates import date2num
        from datetime import timedelta
        import pandas
        fig, ax = plt.subplots()
        plt.xticks(rotation=45)
        plt.yticks()
        ax.set_title('Shanghai 300')
        ax.xaxis_date()
        data_list = []
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("Input param df is not type of DataFrame.")
        for dt, row in df.iterrows():
            t = date2num(dt)
            op, cl, high, low = row[:4]
            # print(dt, row[:4])
            data = (t, op, cl, high, low)
            data_list.append(data)
        try:
            candleplot(
                ax, data_list,
                width=1.0, colorup='r', colordown='green', alpha=0.75)
        except Exception as e:
            pass
        return plt


if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    event = EventView(GLOBAL_HEADER)
    event.get_basic_index('SH000300')