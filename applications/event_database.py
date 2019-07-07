#!/usr/bin/python3

from libmysql8 import MySQLBase, createTable
from form import formStock


def event_initial_database():
    stock = MySQLBase('root', '6414939', 'test')
    createTable(formStock, stock.engine)


if __name__ == '__main__':
    event_initial_database()
