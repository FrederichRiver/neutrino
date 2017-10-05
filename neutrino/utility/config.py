'''
Created on Apr 23, 2017

@author: frederich
'''
from ConfigParser import ConfigParser
import time
import pandas as pd
import urllib2
import requests
from io import StringIO

def openCSV(url,coding):
    resp=urllib2.urlopen(url,timeout=10)
    csv_content=resp.read().decode(coding)
    mMatrix=StringIO(csv_content)
    return pd.read_csv(mMatrix)

def requestCSV(url):
    resp = requests.get(url)
    return pd.read_csv(StringIO(resp.text))

def openPage(url):
    return urllib2.urlopen(url,timeout=10)

def readAccount(filename='config'):
    try:
        cf=ConfigParser()
        cf.read(filename)
        acc=cf.get('db','ACC')
        pw=cf.get('db','PW')
        return acc,pw
    except:
        return None
def dateStr(t=time.localtime()):
    return time.strftime('%Y-%m-%d',t)
def strDate(objstr):
    try:
        return objstr.replace('-','')
    except:
        return '00000000'
def int2Date(date):
    if len(str(date))==7:
        return str(date)[:3]+'-'+str(date)[4:5]+'-'+str(date)[6:]

def readUrl(query,filename='config'):
    try:
        cf=ConfigParser()
        cf.read(filename)
        url=cf.get('url',query)
        return url
    except:
        return None
def readDbDef(query,filename='config'):
    try:
        cf=ConfigParser()
        cf.read(filename)
        DBdef=cf.get('DBdef',query)
        return DBdef
    except:
        return None
def netEaseIndex(index):
    if index[0:2]=='SH':
        return index.replace('SH','0')
    elif index[0:2]=='SZ':
        return index.replace('SZ','1')  
    else:
        return None
def readFloat(objstr):
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
