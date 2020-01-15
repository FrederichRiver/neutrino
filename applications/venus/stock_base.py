#!/usr/bin/python3
import re
from datetime import date
from dev_global.env import TIME_FMT
from msg import NoneHeaderError
from polaris.mysql8 import (mysqlBase, mysqlHeader)


class StockEventBase(object):
    def __init__(self, header):
        self.Today = date.today().strftime(TIME_FMT)
        self.today = date.today().strftime('%Y%m%d')
        if not header:
            raise Exception
        self.mysql = mysqlBase(header)
        self.stock_list = []
        self.coder = StockCodeFormat()

    def __str__(self):
        return "<Stock Event Base>"

    def update_date_time(self):
        """
        Get date of today.
        """
        self.Today = date.today().strftime(TIME_FMT)

    def close(self):
        self.mysql.engine.close()


class StockCodeFormat(object):
    def __call__(self, stock_code):
        if type(stock_code) == str:
            # format <SH600000> or <SZ000001>
            stock_code = stock_code.upper()
            if re.match(r'(\d{6}).([A-Z][A-Z])\Z', stock_code):
                # format <600000.SH> or <000001.SZ>
                result = re.match(r'(\d{6}).([A-Z][A-Z]\Z)', stock_code)
                stock_code = result.group(2)+result.group(1)
            else:
                stock_code = None
            return stock_code

    def net_ease_code(self, stock_code):
        """
        input: SH600000, return: 0600000\n;
        input: SZ000001, return: 1000001.
        """
        stock_code = self.__call__(stock_code)
        if type(stock_code) == str:
            if stock_code[:2] == 'SH':
                stock_code = '0' + stock_code[2:]
            elif stock_code[:2] == 'SZ':
                stock_code = '1' + stock_code[2:]
            else:
                stock_code = None
        else:
            stock_code = None
        return stock_code
