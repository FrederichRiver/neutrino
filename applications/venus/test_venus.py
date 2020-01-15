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


if __name__ == "__main__":
    unit_test_NoneHeaderError()
    unit_test_stockEventBase()
