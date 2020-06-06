#!/usr/bin/python3
from venus.stock_base import StockEventBase


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

    def flag_index(self, stock_code):
        from venus.form import formStockManager
        result = self.mysql.session.query(
            formStockManager.stock_code,
            formStockManager.flag
            ).filter_by(stock_code=stock_code)
        if result:
            result.update(
                {"flag": 'i'}
            )
            self.mysql.session.commit()
        return 1

    def flag_stock(self, stock_code):
        from venus.form import formStockManager
        result = self.mysql.session.query(
            formStockManager.stock_code,
            formStockManager.flag
            ).filter_by(stock_code=stock_code)
        if result:
            result.update(
                {"flag": 't'}
            )
            self.mysql.session.commit()
        return 1

    def flag_b_stock(self, stock_code):
        from venus.form import formStockManager
        result = self.mysql.session.query(
            formStockManager.stock_code,
            formStockManager.flag
            ).filter_by(stock_code=stock_code)
        if result:
            result.update(
                {"flag": 'b'}
            )
            self.mysql.session.commit()
        return 1

    def flag_hk_stock(self, stock_code):
        from venus.form import formStockManager
        result = self.mysql.session.query(
            formStockManager.stock_code,
            formStockManager.flag
            ).filter_by(stock_code=stock_code)
        if result:
            result.update(
                {"flag": 'h'}
            )
            self.mysql.session.commit()
        return 1


if __name__ == "__main__":
    import re
    from dev_global.env import GLOBAL_HEADER
    from venus.stock_flag import EventStockFlag
    event = EventStockFlag(GLOBAL_HEADER)
    stock_list = event.get_all_security_list()
    for stock_code in stock_list:
        if re.match(r'^SH000|^SH950|^SZ399', stock_code):
            event.flag_index(stock_code)
