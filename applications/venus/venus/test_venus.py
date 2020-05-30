from msg import NoneHeaderError
from stock_base import StockEventBase, dataLine


def unit_test_NoneHeaderError():
    try:
        raise NoneHeaderError('Test!')
    except NoneHeaderError as e:
        print(e)


def unit_test_stockEventBase():
    from dev_global.env import GLOBAL_HEADER
    import pandas as pd
    event = StockEventBase(GLOBAL_HEADER)
    try:
        print(event)
        event.update_date_time()
        event.get_all_stock_list()
    except Exception as e:
        print(e)


def unit_test_StockList():
    from stock_base import StockList
    event = StockList()
    event.get_sh_stock()
    stock_list = event.get_sz_stock()
    print(stock_list[0], stock_list[-1])


def unit_test_stock_interest():
    from dev_global.env import GLOBAL_HEADER
    from stock_interest import EventInterest
    import numpy as np
    event = EventInterest(GLOBAL_HEADER)
    event.get_all_stock_list()
    for stock_code in event.stock_list:
        try:
            print(stock_code)
            tab = event.resolve_table(stock_code)
            tab.replace(['--'], np.nan, inplace=True)
            tab.to_sql(
                    'test_interest', event.mysql.engine.connect(),
                    if_exists="append", index=True
                    )
        except Exception:
            print(f"Error while recording interest of {stock_code}")


def unit_test_dataline():
    import pandas as pd
    df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6],
        'name': ['Alice', 'Bob', 'Cindy', 'Eric', 'Helen', 'Grace'],
        'math': [90, 89, 99, 78, 97, 93],
        'english': [89, 94, 80, 94, 94, 90]})
    dt = dataLine('test_interest')
    sql_list = dt.insert_sql(df)
    sql_list = dt.update_sql(df, ['id', 'name'])
    for sql in sql_list:
        print(sql)


def unit_test_financeReport():
    from dev_global.env import GLOBAL_HEADER
    from finance_report import EventFinanceReport
    event = EventFinanceReport(GLOBAL_HEADER)
    event.update_balance_sheet("SH601818")


def unit_test_stockcode():
    from venus.stock_base import StockCodeFormat
    event = StockCodeFormat()
    call_result = event('600000.SH')
    func_result = event.net_ease_code('SH601818')
    print(call_result)
    print(func_result)

def unit_test_absolute_path():
    from venus.stock_manager import absolute_path
    x = 'path/path2/path3'
    y = 'path/path2/path3/'
    z = 'path4/file'
    z2 = '/path4/file'
    print(absolute_path(x,z))
    print(absolute_path(x,z2))
    print(absolute_path(y,z))
    print(absolute_path(y,z2))

if __name__ == "__main__":
    # unit_test_NoneHeaderError()
    # unit_test_stockEventBase()
    # unit_test_StockList()
    # unit_test_stock_interest()
    # unit_test_dataline()
    # unit_test_financeReport()
    unit_test_stockcode()
