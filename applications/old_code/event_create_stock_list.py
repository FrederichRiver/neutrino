#!/usr/bin/python3

# encode = 'wAKO0tFJ8ZH38RW4WseZnQ=='

from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base
from libmysql import MySQLBase

formBase = declarative_base()


class formStockList(formBase):
    __tablename__ = 'stock_list'
    stock_code = Column(String(10), primary_key=True)
    stock_name = Column(String(10))
    gmt_create = Column(Date)
    gmt_modified = Column(Date)


if __name__ == '__main__':
    test = MySQLBase('root', '6414939', 'stock')
    test.create_table(formStockList)
