#!/usr/bin/python3
import json
from datetime import *
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


def opencsv(url):
    return read_csv(url)


def err(text):
    pass

def today():
    td = datetime.now()
    return td.strftime('%Y%m%d')

if __name__ == '__main__':
    # print(readurl('URL_163_MONEY'))
    print(neteaseindex('SZ002230'))
    print(neteaseindex('SH601818'))
    print(today())
