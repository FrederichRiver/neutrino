#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from libmysql8 import mysqlHeader, mysqlBase, create_table
from form import formTemplate


def event_initial_database():
    header = mysqlHeader('root', '6414939', 'test')
    mysql = mysqlBase(header)
    create_table(formTemplate, mysql.engine)

# event back up


def event_database_backup():
    pass

# modify tables batchly


def table_batch_modify():
    pass


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
    else:
        pass
