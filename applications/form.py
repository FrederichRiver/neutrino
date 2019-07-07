#!/usr/bin/python3
from sqlalchemy.engine.url import URL as engine_url
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base

formBase = declarative_base()
formStock = declarative_base()


class formStockList(formBase):
    __tablename__ = 'stock_list'
    stock_code = Column(String(10), primary_key=True)
    stock_name = Column(String(10))
    gmt_create = Column(Date)
    gmt_modified = Column(Date)

    def __repr__(self):
        return None


class formStock(formStock):
    __tablename__ = 'stock'
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


class formFinanceReport(formBase):
    __tablename__ = 'finance_report'
    name = Column(String(10), primary_key=True)

    def __repr__(self):
        pass
