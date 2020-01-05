#!/usr/bin/env python
# -*- coding: utf-8 -*-


def unit_test_str2num():
    from utils import str2number
    num_list = ['2019-09-23','+0.6','0.7','-0.35','3','-5','128', '-137', '156.01', '-1789.22', '13,791.02', '$800', '$237.5', 'xs678.5', '192,138.00w']
    for num in num_list:
        print(num, ': ', str2number(num))


def unit_test_random_header():
    from utils import RandomHeader
    rh = RandomHeader()
    for i in range(15):
        print(rh())


def test():
    from env import global_header
    from utils import RandomHeader
    from dev import TotalStock
    import pandas as pd
    import numpy as np
    event = TotalStock()
    event._init_database(global_header)
    result = event.mysql.select_values2('SH600001', 'trade_date,stock_quantity')
    result.columns = ['trade_date', 'quantity']
    result.astype({'quantity': np.float64}).dtypes
    print(result.head(5))
    print(result.dtypes)


if __name__ == "__main__":
    # unit_test_random_header()
    test()
