#!/usr/bin/python3
"""
Geschafen im Aug 31, 2017

Verfasst von Friederich Fluss
"""
__version__ = '3.0.6-alpha'

# encode = 'wAKO0tFJ8ZH38RW4WseZnQ=='

#from libmysql import MySQLBase
from sqlalchemy.orm import mapper
from sqlalchemy import Table, MetaData
from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL as engine_url
from sqlalchemy import create_engine
formBase = declarative_base()
stock_code = ''
print(type(formBase))


class formStock(formBase):
    __tablename__ = 'stock_code'
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
        return ''


class MySQLBase(object):
    def __init__(self, acc, pw, database, host='localhost', port=3306):
        DB_STRING = engine_url('mysql+pymysql',
                               username=acc,
                               password=pw,
                               host=host,
                               port=port,
                               database=database)
        self.engine = create_engine(DB_STRING, echo=True)

    def create_table(self, form):
        form.metadata.create_all(self.engine)

    def batch_create_table(self, name, form):
        t = type(name, (object,), dict())
        metadata = MetaData()
        Stock = Table(name, metadata,
                      Column('trade_date', Date,
                             primary_key=True),
                      Column('close_price', Float(precision=10,
                                                  decimal_return_scale=3)),
                      Column('high_price', Float(precision=10,
                                                 decimal_return_scale=3)),
                      Column('low_price', Float(precision=10,
                                                decimal_return_scale=3)),
                      Column('open_price', Float(precision=10,
                                                 decimal_return_scale=3)),
                      Column('yesterday_price', Float(precision=10,
                                                      decimal_return_scale=3)),
                      Column('amplitude', Float(precision=5,
                                                decimal_return_scale=3)),
                      Column('volumn', Integer),
                      Column('value', Integer))

        mapper(t, Stock)
        return t


if __name__ == '__main__':
    test = MySQLBase('root', '6414939', 'test')
    x = test.batch_create_table('test_table', formStock)
    print(x)
    x.metadata.create_all(test.engine)
