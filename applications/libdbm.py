#!/usr/bin/python3
'''
Created on Jan 27, 2019

@Author: Friederich Fluss
    
@Version:
v1.0.0-beta, Jan 27, 2019, first released.
'''
import functools
from libbase import *
from libmysql8 import MySQLServer
import libencrypt
import time
from libstock import *
__version__ = '1.0.1-beta'

def del_stock_code(table_name):
    fin = MySQLServer('root', '6414939','finance')
    stk = MySQLServer('root', '6414939', 'stock_data')
    try:
        stk.dropTable(table_name)
    except:
        pass
    fin.rmData('stock_index', "stock_code='{0}'".format(table_name)) 

def _DEL_ALL_STOCK():
    print('OPERATION WILL DELETE ALL STOCKS!')
    stkd = MySQLServer('root', '6414939','finance')
    temp_list = queryindex(stkd)
    print(temp_list[:10])
    for code in temp_list:
        del_stock_code(code)
    
if __name__ == '__main__':
    _DEL_ALL_STOCK()
