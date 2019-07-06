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

__version__ = '3.0.6-alpha'


from sqlalchemy.engine.url import URL as engine_url
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import sessionmaker
formBase = declarative_base()
formStock = declarative_base()


class formStockList(formBase):
    __tablename__ = 'stock_list'
    stock_code = Column(String(10), primary_key=True)
    stock_name = Column(String(10))
    gmt_create = Column(Date)
    gmt_modified = Column(Date)


class formStock(formStock):
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
    __tablename__ = 'finance_report'
    name = Column(String(10), primary_key=True)

    def __repr__(self):
        pass


class MySQLBase(object):
    def __init__(self, acc, pw, database, host='localhost'):
        self.charset = 'utf8'
        self.port = 3306
        DB_STRING = f'mysql+pymysql://{acc}:{pw}@{host}:{self.port}/{database}'
        self.engine = create_engine(DB_STRING, echo=True)
        DB_session = sessionmaker(bind=self.engine)
        self.session = DB_session()

def createTablefromTable(name, tableName, engine):
    Base = declarative_base()
    Base.metadata.reflect(engine)
    table = Base.metadata.tables[tableName]
    c = str(CreateTable(table))
    c = c.replace("CREATE TABLE", "CREATE TABLE if not exists")
    c = c.replace('"'+tableName+'"', name)
    engine.connect().execute(c)
    engine.connect().close()
    Base.metadata.clear()


def createTable(base, engine):
    base.metadata.create_all(engine)


def dropAll(base, engine):
    base.metadata.drop_all(engine)


if __name__ == '__main__':
    test = MySQLBase('root', '6414939', 'test')
    createTable(formBase, test.engine)
    # createTablefromTable('report5', 'financeReport', test.engine)
    createTable(formBase, test.engine)
