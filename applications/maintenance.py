#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libmysql8 import mysqlHeader, mysqlBase, create_table
from form import formTemplate


def event_initial_database():
    header = mysqlHeader('root', '6414939', 'test')
    stock = mysqlBase(header)
    create_table(formTemplate, stock.engine)

# event back up


def event_database_backup():
    pass

# modify tables batchly


def table_batch_modify():
    pass


if __name__ == "__main__":
    event_initial_database()
