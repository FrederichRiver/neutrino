#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from libmysql8 import mysqlHeader, mysqlBase, create_table
from form import (
    formTemplate,  formStockManager,
    formFinanceTemplate, formInfomation)
from libstock import StockEventBase

__version__ = '1.4'


def event_initial_database(header):
    mysql = mysqlBase(header)
    create_table(formTemplate, mysql.engine)
    create_table(formFinanceTemplate, mysql.engine)
    create_table(formInfomation, mysql.engine)


def event_drop_tables(header):
    mysql = mysqlBase(header)
    # self definition
    table_list = mysql.session.query(
            formStockList.stock_code
            ).filter_by(flag='0').all()
    for dataline in table_list:
        table_name = "{}_interest".format(dataline[0])
        print(table_name)
        mysql.drop_table(table_name)

# event back up


def event_database_backup():
    pass

# modify tables batchly


def table_batch_modify():
    header = mysqlHeader('root', '6414939', 'test')
    # self definition
    event = StockEventBase()
    event._init_database(header)
    stock_list = event.fetch_all_stock_list()
    for stock in stock_list:
        print(stock)
        try:
            sql = f"alter table {stock} add column adjust_factor float"
            event.mysql.engine.execute(sql)
        except Exception:
            pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("maint init|backup")
        raise SystemExit(1)
    if sys.argv[1] == "init":
        try:
            header = mysqlHeader('stock', 'stock2020', 'stock')
            event_initial_database(header)
        except Exception as e:
            print(e)
    elif sys.argv[1] == "backup":
        try:
            event_database_backup()
        except Exception as e:
            print(e)
    elif sys.argv[1] == "test":
        try:
            table_batch_modify()
        except Exception as e:
            print(e)
    else:
        pass
