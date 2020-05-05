#!/usr/bin/python3

from venus.stock_base import StockEventBase
from dev_global.env import GLOBAL_HEADER


class EventFundamental(StockEventBase):
    def __init__(self, header):
        super(EventFundamental, self).__init__(header)


    def quarter_profit(self, stock_code, report_period):
        result = self.mysql.condition_select(
            "income_statement_sheet", "r4_net_profit",
            f"stock_code='{stock_code}' and report_period='{report_period}'"  
        )
        return result


if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    event = EventFundamental(GLOBAL_HEADER)
    result = event.quarter_profit('SH600000', '2019-12-31')
    print(result)
