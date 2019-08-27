#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libstock import StockEventBase 

if __name__ == "__main__":
    # dataline testing
    """
    input_string = ['2008-07-01', '2007',
                    '0', '0', '1.50',
                    '2008-07-04', '2008-07-07', '--']
    dt = dataline()
    result = dt.resolve(input_string, 'SH600001_interest')
    print(result)
    """
    # event create interest tables
    # event_create_interest_table()
    # event record interest
    # event_record_interest()
    from libmysql8 import mysqlHeader
    header = mysqlHeader('root', '6414939', 'test')
    stock_event = StockEventBase(header)
    print(stock_event)
