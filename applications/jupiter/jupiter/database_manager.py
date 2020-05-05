#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from dev_global.env import GLOBAL_HEADER
from polaris.mysql8 import mysqlHeader, mysqlBase, create_table
from venus.stock_base import StockEventBase


__version__ = '1.1.6'
__all__ = ['event_mysql_backup', 'event_initial_database']


# event back up


class databaseBackup(object):
    def __init__(self):
        self.database_list = []
        # self.temp_path = '/home/friederich/Downloads/tmp/'
        # self.backup_path = '/home/friederich/Downloads/neutrino/'
        self.temp_path = '/root/tmp/'
        self.backup_path = '/root/backup/'
        self.user = 'root'
        self.pwd = '6414939'

    def get_database_list(self):
        self.database_list = ['stock', 'natural_language']
        return self.database_list

    def backup(self):
        for db in self.database_list:
            print(f"Now starting backup database {db}.")
            dumpcmd = (
                f"mysqldump -u {self.user} "
                f"--password={self.pwd} "
                f"--databases {db}"
                f" > {self.temp_path}{db}.sql"
                )
            os.system(dumpcmd)

    def compress(self):
        import time
        for db in self.database_list:
            zip_time = time.strftime('%Y-%m-%d')
            compress_file = f"{self.backup_path}{db}_{zip_time}.tar.gz"
            print(compress_file)
            compress_cmd = f"tar -czvPf {compress_file} {self.temp_path}"
            print(compress_cmd)
            os.chdir(self.backup_path)
            os.system("pwd")
            os.system(compress_cmd)
        # print("compress complete!")
        # remove_cmd = f"rm -rf {backup_path}"
        # os.system(remove_cmd)

    def remove_old_backup(self):
        import re
        file_list = os.listdir(self.backup_path)
        temp_list = {}
        for f in file_list:
            file_name, file_time = self.get_backup_time(self.backup_path + f)
            temp_list[file_name] = file_time

    def get_backup_time(self, file_name):
        import re
        import time
        from dev_global.env import TIME_FMT
        import os
        result = os.stat(file_name)
        return file_name, result.st_mtime


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
        event.backup()
        event.compress()
    except Exception:
        ERROR("Database backup failed.")


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
