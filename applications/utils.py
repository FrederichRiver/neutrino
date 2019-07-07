#!/usr/bin/python3
import json
import logging
from datetime import datetime
from pandas import read_csv


def readurl(url):
    with open('config/conf.json', 'r') as f:
        result = f.read()
        j = json.loads(result)
    return j[url]


def neteaseindex(code):
    if code[:2] == 'SH':
        code = '0'+code[2:]
    else:
        code = '1'+code[2:]
    return code


def opencsv(url, encoding):
    return read_csv(url, encoding=encoding)


def recordBase(text, level=logging.INFO):
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


def today():
    return datetime.now().strftime('%Y%m%d')


if __name__ == '__main__':
    print(readurl('URL_163_MONEY'))
    print(neteaseindex('SZ002230'))
    print(neteaseindex('SH601818'))
    print(today())
    recordBase('text')
