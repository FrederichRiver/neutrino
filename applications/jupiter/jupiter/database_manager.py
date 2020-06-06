#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from dev_global.env import GLOBAL_HEADER
from polaris.mysql8 import create_table, mysqlBase, mysqlHeader
from venus.stock_base import StockEventBase

__version__ = '1.1.6'
__all__ = ['event_mysql_backup', 'event_initial_database']


# event back up


class databaseBackup(object):
    def __init__(self):
        import os
        flag = os.environ.get('LOGNAME')
        self.database_list = []
        if flag == 'friederich':
            self.temp_path = '/home/friederich/Downloads/tmp/'
            self.backup_path = '/home/friederich/Downloads/neutrino/'
        else:
            self.temp_path = '/root/tmp/'
            self.backup_path = '/root/backup/'
        self.user = 'root'
        self.pwd = '6414939'

    def get_database_list(self):
        self.database_list = ['stock', 'natural_language']
        return self.database_list

    def database_backup(self):
        for db in self.database_list:
            dumpcmd = (
                f"mysqldump -u {self.user} "
                f"--password={self.pwd} "
                f"--databases {db}"
                f" > {self.temp_path}{db}.sql"
                )
            os.system(dumpcmd)

    def file_compress(self):
        import time
        zip_time = time.strftime('%Y-%m-%d')
        file_name = 'mysql_database'
        compress_file = f"{self.backup_path}{fine_name}_{zip_time}.tar.gz"
        os.chdir(self.backup_path)
        os.system(f"tar -czvPf {compress_file} {self.temp_path}")

    def remove_old_backup(self):
        import re
        import datetime
        file_list = os.listdir(self.backup_path)
        for f in file_list:
            file_name, file_time = self.get_file_info(self.backup_path + f)
            if file_time < self.get_today_time(3):
                os.system(f"rm {file_name}")

    def get_today_time(self, n=0):
        import datetime
        timestamp = datetime.datetime.now()
        dest_time = timestamp - datetime.timedelta(days=n)
        return dest_time        

    def get_file_info(self, file_name):
        """
        get timestamp from file info.
        return type timestamp
        """
        import os
        import datetime
        result = os.stat(file_name)
        file_time = datetime.datetime.fromtimestamp(result.st_mtime)
        return file_name, file_time


def event_initial_database():
    from dev_global.env import GLOBAL_HEADER
    from jupiter.utils import ERROR
    from polaris.mysql8 import create_table, mysqlBase, mysqlHeader
    from venus.form import formTemplate, formFinanceTemplate, formInfomation
    try:
        # root_header = mysqlHeader('root', '6414939', 'stock')
        # mysql = mysqlBase(root_header)
        mysql = mysqlBase(GLOBAL_HEADER)
        create_table(formTemplate, mysql.engine)
        create_table(formFinanceTemplate, mysql.engine)
        create_table(formInfomation, mysql.engine)
    except Exception as e:
        ERROR(e)
        ERROR("Database initialize failed.")


def event_mysql_backup():
    from jupiter.database_manager import databaseBackup
    from jupiter.utils import ERROR
    try:
        event = databaseBackup()
        event.get_database_list()
        event.database_backup()
        event.compress_file()
    except Exception:
        ERROR("Database backup failed.")


def event_mysql_remove_backup():
    from jupiter.database_manager import databaseBackup
    event = databaseBackup()
    event.remove_old_backup()


def change_stock_template_definition():
    from dev_global.env import GLOBAL_HEADER
    from polaris.mysql8 import mysqlHeader
    from venus.stock_base import StockEventBase
    root_header = mysqlHeader('stock', 'stock2020', 'stock')
    event = StockEventBase(root_header)
    stock_list = event.get_all_stock_list()
    col = ['close_price','highest_price', 'lowest_price','open_price','prev_close_price','change_rate','amplitude','turnover']
    for stock_code in stock_list:
        # print(stock_code)
        for name in col:
            sql = f"alter table {stock_code} change {name} {name} float default 0"
            event.mysql.engine.execute(sql)
        sql = f"alter table {stock_code} change volume volume int(11) default 0"
        event.mysql.engine.execute(sql)
        sql = f"alter table {stock_code} change adjust_factor adjust_factor float default 1"
        event.mysql.engine.execute(sql)

def test():
    event = databaseBackup()
    event.remove_old_backup()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("maint init|backup")
        raise SystemExit(1)
    if sys.argv[1] == "init":
        try:
            event_initial_database()
        except Exception as e:
            print(e)
    elif sys.argv[1] == "backup":
        try:
            event_database_backup()
        except Exception as e:
            print(e)
    elif sys.argv[1] == "test":
        test()
