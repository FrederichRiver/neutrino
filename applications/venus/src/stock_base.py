#!/usr/bin/python3
import re
from datetime import date
from dev_global.env import TIME_FMT
from venus.msg import NoneHeaderError
from polaris.mysql8 import (mysqlBase, mysqlHeader)


__version__ = '1.0.10'


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


class StockList(object):
    def __init__(self):
        pass

    def get_sh_stock(self):
        stock_list = [f"SH60{str(i).zfill(4)}" for i in range(4000)]
        return stock_list

    def get_sz_stock(self):
        stock_list = [f"SZ{str(i).zfill(6)}" for i in range(1, 1000)]
        return stock_list

    def get_cyb_stock(self):
        stock_list = [f"SZ300{str(i).zfill(3)}" for i in range(1, 1000)]
        return stock_list

    def get_zxb_stock(self):
        stock_list = [f"SZ002{str(i).zfill(3)}" for i in range(1, 1000)]
        return stock_list

    def get_b_stock(self):
        s1 = [f"SH900{str(i).zfill(3)}" for i in range(1, 1000)]
        s2 = [f"SZ200{str(i).zfill(3)}" for i in range(1, 1000)]
        stock_list = s1 + s2
        return stock_list

    def get_index(self):
        index1 = [f"SH000{str(i).zfill(3)}" for i in range(1000)]
        index2 = [f"SH950{str(i).zfill(3)}" for i in range(1000)]
        index3 = [f"SZ399{str(i).zfill(3)}" for i in range(1000)]
        stock_list = index1 + index2 + index3
        return stock_list

    def get_kcb_stock(self):
        stock_list = [f"SH688{str(i).zfill(3)}" for i in range(1000)]
        return stock_list

    def get_xsb_stock(self):
        pass

    def get_stock(self):
        stock_list = self.get_sh_stock()
        stock_list += self.get_sz_stock()
        stock_list += self.get_cyb_stock()
        stock_list += self.get_zxb_stock()
        return stock_list
