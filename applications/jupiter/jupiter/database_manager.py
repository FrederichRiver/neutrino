#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from polaris.mysql8 import mysqlHeader, mysqlBase, create_table
# from form import (
#    formTemplate,  formStockManager,
#    formFinanceTemplate, formInfomation)
from venus.stock_base import StockEventBase
from dev_global.env import GLOBAL_HEADER


__version__ = '1.4'

"""
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
"""
# event back up


class databaseBackup(object):
    def __init__(self):
        self.database_list = []
        self.temp_path = '/home/friederich/Downloads/tmp'
        self.backup_path = '/home/friederich/Downloads/neutrino'
        self.user = 'root'
        self.pwd = '6414939'

    def get_database_list(self):
        self.database_list = ['stock']
        return self.database_list

    def backup(self):
        for db in self.database_list:
            print(f"Now starting backup database {db}.")
            dumpcmd = (
                f"mysqldump -u {self.user} "
                f"--password={self.pwd} "
                f"--databases {db}"
                f" > {self.temp_path}/{db}.sql"
                )
            os.system(dumpcmd)

    def compress(self):
        import time
        for db in self.database_list:
            compress_file = f"{self.backup_path}/{db}_{time.strftime('%Y-%m-%d_%H:%M:%S')}.tar.gz"
            print(compress_file)
            compress_cmd = f"tar -czvPf {compress_file} {self.temp_path}"
            print(compress_cmd)
            os.chdir(self.backup_path)
            os.system("pwd")
            os.system(compress_cmd)
        print("compress complete!")
        # remove_cmd = f"rm -rf {backup_path}"
        # os.system(remove_cmd)

    def remove_old_backup(self):
        import re
        file_list = os.listdir(self.backup_path)
        for f in file_list:
            m = re.match(r'(\w+)_(\d{4}\-\d{2}\-\d{2}_\d{2}:\d{2}:\d{2})\.(tar\.gz)', f)
            if m:
                self.get_backup_time(f)

    def get_backup_time(self, file_name):
        import re, time
        # (\d{1,2}):(\d{2})
        m = re.match(r'(\w+)_(\d{4}\-\d{2}\-\d{2})', file_name)
        if m:
            t = time.strftime(m.group(2))
            print(t)


def event_database_backup():
    pass

# modify tables batchly

"""
def table_batch_modify():
    header = mysqlHeader('root', '6414939', 'test')
    # self definition
    event = StockEventBase()
    event._init_database(header)
    stock_list = event.fetch_all_stock_list()
    for stock in stock_list:
        print(stock)
        try:
            sql = f"alter table {stock} add column stock_quantity int"
            event.mysql.engine.execute(sql)
        except Exception:
            pass
"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("maint init|backup")
        raise SystemExit(1)
    if sys.argv[1] == "init":
        try:
            # header = mysqlHeader('stock', 'stock2020', 'stock')
            header = mysqlHeader('root', '6414939', 'test')
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
            bk = databaseBackup()
            bk.get_database_list()
            bk.backup()
        except Exception as e:
            print(e)
    else:
        pass
