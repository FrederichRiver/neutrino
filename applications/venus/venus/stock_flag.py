#!/usr/bin/python3
import json
from venus.stock_base import StockEventBase
from dev_global.env import GLOBAL_HEADER
# from jupiter.network import RandomHeader
import requests


class EventStockFlag(StockEventBase):
    def flag_quit_stock(self, stock_code):
        import datetime
        import pandas as pd
        from datetime import date
        from dev_global.env import TIME_FMT
        result = self.mysql.select_values(stock_code, 'trade_date')
        if not result.empty:
            result = result[0].tolist()
            d = datetime.date.today() - result[-1]
            if d.days > 150:
                return True
            else:
                return False
        else:
            return False


if __name__ == "__main__":
    pass
