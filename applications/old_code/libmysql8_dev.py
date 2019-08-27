#!/usr/bin/python3
"""
Geschafen im Aug 31, 2017

Verfasst von Friederich Fluss

Lib of mysql contains methods to drive mysql db using python.
v1.0.0-stable: Library is released.
v1.0.1-stable: Encrypted password is supported, relative codes are in
libencrypt.
v1.0.2-stable: Add new function TABLEEXIST.
v2.0.3-dev: Complete funcions of mysql.
v2.0.4-dev: Modify some bug, using encrypt pw.
v2.0.5-dev: Fix bug. drop table -> drop table if exists.
v3.0.6-alpha: change personal engine into commercial engine sqlalchemy.
"""

"""
X2.exit
4.grant db to user
X7.drop database
X9.use database
X10.select now
15.delete from table where
17.multi table update
*18.alter table add index
20.alter table add unique index
25.rename table
26.database backup
"""
#from applications.libencrypt import mydecrypt

__version__ = '3.0.6-alpha'

# encode = 'wAKO0tFJ8ZH38RW4WseZnQ=='

from sqlalchemy.engine.url import URL as engine_url
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
formBase = declarative_base()


class formStockList(formBase):
    __tablename__ = 'stock_list'
    stock_code = Column(String(10), primary_key=True)
    stock_name = Column(String(10))
    gmt_create = Column(Date)
    gmt_modified = Column(Date)
"""

class formStock(formBase):
    __tablename__ = 'stock_index'
    trade_date = Column(Date, primary_key=True)
    close_price = Column(Float(precision=10,
                               decimal_return_scale=3))
    high_price = Column(Float(precision=10,
                              decimal_return_scale=3))
    low_price = Column(Float(precision=10,
                             decimal_return_scale=3))
    open_price = Column(Float(precision=10,
                              decimal_return_scale=3))
    yesterday_price = Column(Float(precision=10,
                                   decimal_return_scale=3))
    amplitude = Column(Float(precision=5,
                             decimal_return_scale=3))
    volume = Column(Integer)
    value = Column(Integer)

    def __repr__(self):
        return f'{stock} is created at {time} and be modified at {time2}'


class formFinanceReport(formBase):
    __tablename__ = 'financeReport'
    name = Column(String(10), primary_key=True)

    def __repr__(self):
        pass
"""

class MySQLBase(object):
    def __init__(self, acc, pw, database, host='localhost'):
        charset = 'utf8'
        port = 3306
        DB_STRING = f'mysql+pymysql://{acc}:{pw}@{host}:{port}/{database}'
        self.engine = create_engine(DB_STRING)

    def create_stock_index_table(self):
        stock_list = formStockList()
        stock_list.metadata.create_all(self.engine)


if __name__ == '__main__':
    test = MySQLBase('root', '6414939', 'stock')
    test.create_stock_index_table()
