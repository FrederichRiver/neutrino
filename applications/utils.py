#!/usr/bin/python3
import json
import logging
from datetime import datetime
from pandas import read_csv
import functools


def read_url(url):
    with open('config/conf.json', 'r') as f:
        result = f.read()
        j = json.loads(result)
    return j[url]


def read_sql(sql_name):
    """load sql from sql.json

    :sql_name: TODO
    :returns: TODO

    """
    with open('config/sql.json', 'r') as f:
        result = f.read()
        j = json.loads(result)
        return j[sql_name]

def neteaseindex(code):
    if code[:2] == 'SH':
        code = '0'+code[2:]
    else:
        code = '1'+code[2:]
    return code


def opencsv(url, encoding):
    import numpy as np
    dcolumns = ['Date', 'Stock_code',
                'Stock_name', 'Close_price',
                'Highest_price', 'Lowest_price',
                'Open_price', 'Prev_close_price',
                'Change', 'Amplitude',
                'Volume', 'Turnover']
    return read_csv(url, encoding=encoding)


def record_base(text, level=logging.INFO):
    logging.basicConfig(filename='neutrino.log',
                        level=logging.INFO,
                        filemode='a',
                        format="%(asctime)s [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    if level == logging.INFO:
        logging.info(text)
    elif level == logging.WARNING:
        logging.warn(text)
    elif level == logging.ERROR:
        logging.error(text)


info = functools.partial(record_base, level=logging.INFO)
error = functools.partial(record_base, level=logging.ERROR)
warning = functools.partial(record_base, level=logging.WARNING)


def today():
    return datetime.now().strftime('%Y%m%d')


if __name__ == '__main__':
    print(read_url('URL_163_MONEY'))
    print(neteaseindex('SZ002230'))
    print(neteaseindex('SH601818'))
    print(today())
    record_base('text')
