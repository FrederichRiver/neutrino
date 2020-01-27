from msg import NoneHeaderError
from stock_base import StockEventBase


def unit_test_NoneHeaderError():
    try:
        raise NoneHeaderError('Test!')
    except NoneHeaderError as e:
        print(e)


def unit_test_stockEventBase():
    from dev_global.env import GLOBAL_HEADER
    event = StockEventBase(GLOBAL_HEADER)
    try:
        print(event)
        event.update_date_time()
    except Exception as e:
        print(e)


def unit_test_StockList():
    from stock_base import StockList
    event = StockList()
    event.get_sh_stock()
    stock_list = event.get_sz_stock()
    print(stock_list[0], stock_list[-1])


if __name__ == "__main__":
    unit_test_NoneHeaderError()
    unit_test_stockEventBase()
    unit_test_StockList()
