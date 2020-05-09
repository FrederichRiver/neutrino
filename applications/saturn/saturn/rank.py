#!/usr/bin/python3

from polaris.mysql8 import mysqlBase
from dev_global.env import VIEWER_HEADER

class data_view_base(object):
    def __init__(self):
        self.mysql = mysqlBase(VIEWER_HEADER)

    def get_data(self):
        raise Exception

    def visualize(self):
        raise Exception

class profit_growth_rate(data_view_base):
    def get_data(self, stock_code):
        result = self.mysql.condition_select(
            'income_statement','report_date,float_c40',f"char_stock_code='{stock_code}'")
        if not result.empty:
            result.columns = ['report_date', 'net_profit']
            result.set_index('report_date', inplace=True)
            result['last_period'] = result['net_profit'].shift(4)
            result['growth_rate'] = result['net_profit']/result['last_period'] - 1
            result.dropna(axis=0, how='any', inplace=True)

            result.drop(['net_profit','last_period'], axis=1, inplace=True)
            result.columns = [f"{stock_code}"]
        return result

    def get_stock_list(self):
        result = self.mysql.condition_select('stock_manager', 'stock_code', "flag='t'")
        return list(result[0])


def profit_growth_analysis():
    import pandas
    # import xlwt
    from datetime import date
    event = profit_growth_rate()
    stock_list = event.get_stock_list()
    profit_data = pandas.DataFrame()
    for stock in stock_list[:10]:
        df = event.get_data(stock)
        profit_data = pandas.concat([profit_data, df], axis=1)
    result = profit_data.T
    result = result.loc[:,[date(2019,9,30),date(2019,12,31),date(2020,3,31)]]
    result.dropna(axis=0, inplace=True)
    result = result.applymap(lambda x: format(x, '.2%'))
    result.insert(0, 'stock_name', result.index)
    for index,row in result.iterrows():
        stock_name = event.mysql.select_one('stock_manager', 'stock_name', f"stock_code='{index}'")
        row['stock_name'] = stock_name[0]
    # result.to_excel('/home/friederich/Downloads/stock_data.xls')
    result = result.sort_values(by=date(2020,3,31),ascending=False)
    print(result)


if __name__ == "__main__":
    profit_growth_analysis()