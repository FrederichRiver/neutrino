#!/usr/bin/python3
import json
import logging
from datetime import datetime
from pandas import read_csv
import functools
import psutil
from env import CONF_FILE,LOG_FILE,SQL_FILE

def read_url(url):
    with open(CONF_FILE, 'r') as f:
        result = f.read()
        j = json.loads(result)
    return j[url]


def read_sql(sql_name):
    """load sql from sql.json

    :sql_name: TODO
    :returns: TODO

    """
    with open(CONF_FILE, 'r') as f:
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
    logging.basicConfig(filename=LOG_FILE,
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



class Resource(object):
    def __init__(self):
        self.cpu = 0.0
        self.memory = 0.0
        self.period = 0.0

    def _query_info(self):
        mem = psutil.virtual_memory()
        self.memory = mem.percent
        self.cpu = psutil.cpu_percent(1)
        return self.cpu, self.memory

    def status(self):
        self._query_info()
        if self.memory < 85:
            return self.memory
        else:
            return 0

    def system_report(self):
        # Report system infomation.
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        MB = 1024*1024
        GB = 1024*MB
        sys_info = (
            f"<CPU>: {psutil.cpu_count()}\n"
            f"<Total Memory>: {round(mem.total/MB, 2)}MB\n"
            f"<Total Disk>: {round(disk.total/GB, 2)}GB"
        )

        return sys_info


if __name__ == '__main__':
    pass
