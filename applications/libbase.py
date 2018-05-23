#!/usr/bin/python3
'''
Created on Apr 23, 2017

Basic functions base on python 3.6.2
@author: Frederich River

Release note
v1.0.0-beta: First release.
v1.0.1-stable: All functions are tested, now they are stable.
'''
__version__ = '1.0.1-stable'

from configparser import ConfigParser
import time
import pandas as pd
import requests
from io import StringIO
import logging
import functools

LOGFILE='neutrino.log'

def logconfig(loggingfile):
    date_format = '%d %b %Y %H:%M:%S'
    format_string = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=format_string,
                        datefmt=date_format,
                        filename=loggingfile,
                        filemode='a')

def infolog(msg,level='INFO'):
    logconfig(LOGFILE)
    if level == 'INFO':
        logging.info(msg)
    elif level == 'WARNING':
        logging.warn(msg)
    elif level == 'ERROR':
        logging.error(msg)
    else:
        logging.info(msg)

info = functools.partial(infolog, level='INFO')
warning = functools.partial(infolog, level='WARNING')
err = functools.partial(infolog, level='ERROR')

def opencsv(url, coding):
    import urllib.request
    resp = urllib.request.urlopen(url,timeout=10)
    csv_content = resp.read().decode(coding)
    mMatrix = StringIO(csv_content)
    return pd.read_csv(mMatrix)

def requestcsv(url):
    resp = requests.get(url)
    return pd.read_csv(StringIO(resp.text))

def openpage(url):
    return urllib2.urlopen(url, timeout=10)

def readacc(filename='config'):
    try:
        cf=ConfigParser()
        cf.read(filename)
        acc=cf.get('db', 'ACC')
        pw=cf.get('db', 'PW')
        return acc, pw
    except Exception as e:
        print(e)
        return None

def date2str(t=time.localtime()):
    return time.strftime('%Y-%m-%d',t)
def time2str(t=time.localtime()):
    return time.strftime('%Y-%m-%d %H:%M:%S',t)
def date2str2(t=time.localtime()):
    return time.strftime('%Y%m%d',t)
def datestring2int(objstr):
    try:
        return objstr.replace('-','')
    except:
        return '00000000'

def int2datestring(date):
    if len(str(date)) == 8:
        return str(date)[:4]+'-'+str(date)[4:6]+'-'+str(date)[-2:]

def readurl(query,filename='config'):
    try:
        cf=ConfigParser()
        cf.read(filename)
        url=cf.get('url',query)
        return url
    except Exception as e:
        print(e)
        return None

def databasedef(query,filename='config'):
    try:
        cf=ConfigParser()
        cf.read(filename)
        dbdef=cf.get('DBDEF',query)
        return dbdef
    except:
        return None

def neteaseindex(index):
    if index[0:2]=='SH':
        return index.replace('SH','0')
    elif index[0:2]=='SZ':
        return index.replace('SZ','1')
    else:
        return None

def readfloat(objstr):
    import re
    try:
        if re.match(r'\-?\d+\.\d+',str(objstr)):
            return float(objstr)
        elif re.match(r'\-?\d+', str(objstr)):
            return int(objstr)
        else:
            return 0.0
    except Exception:
        return 0.0

if __name__ == "__main__":
    print('testing function: readfloat')
    if readfloat('3.5') == 3.5: print('pass')
    if readfloat('x') == 0.0: print('pass')
    if readfloat('1') == 1 : print('pass')
    print('testing function: neteaseindex')
    print('0601818', neteaseindex('SH601818'))
    print('1000625', neteaseindex('SZ000625'))
    print('None', neteaseindex('MY763'))
    print('testing function: int2datesting')
    print('2018-02-12', int2datestring(20180212))
    print('2018-02-12', int2datestring('20180212'))
    print('None', int2datestring(180212))
    print('testing function: datestring2int')
    print('20180205', datestring2int('2018-02-05'))
    print('today', datestring2int('today'))
    print('180205', datestring2int('18-02-05'))
    print('testing function: readurl')
    print(readurl('URL_NE_INDEX'))
    print(readurl('URL_NE_STOCK'))
    print('testing function: databasedef')
    print(databasedef('DEF_INDEX'))
    print('testing function: infolog')
    info('info test')
    warning('warning test')
    err('error test')
