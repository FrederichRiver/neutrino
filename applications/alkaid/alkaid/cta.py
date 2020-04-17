#!/usr/bin/python3
# from strategy_base import strategyBase
from venus.stock_base import StockEventBase
from dev_global.env import GLOBAL_HEADER


class strategyBase(StockEventBase):
    def __init__(self):
        super(strategyBase, self).__init__(GLOBAL_HEADER)

    def _get_data(self):
        pass

    def _settle(self):
        pass


class new_cta(strategyBase):
    def _get_data(self):
        stock_list = self.get_all_stock_list()
        for stock in stock_list:
            self.condition_1(stock)

    def condition_1(self, stock_code):
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